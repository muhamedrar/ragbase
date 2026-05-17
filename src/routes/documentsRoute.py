from fastapi import APIRouter, Depends,status, Request, UploadFile, File, Form , BackgroundTasks
import os
from pathlib import Path
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseEnums
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from helpers.settings import Settings, get_settings
from controllers.department_controller import DepartmentController
from controllers.document_controller import DocumentController
from repositories.document_repository import  DocumentRepository
from repositories.department_repository import  DepartmentRepository
from repositories.chunk_repository import  ChunkRepository
from models.db_schema.document import Document
from controllers.chunk_controller import ChunckController
from services.EmbeddingService import EmbeddingService


router = APIRouter(
    prefix="/document",
    tags=["document"]
)


@router.post("/process")
async def upload_document(
  request:Request,
  background_tasks: BackgroundTasks,
  department_id:int = Form(...),
  chunk_size:int = 500,
  chunk_overlap:int = 100,
  do_reset:int = Form(1),
  file : UploadFile = File(...),
  session: AsyncSession = Depends(get_db_session),
  settings : Settings=  Depends(get_settings),
):

  document_repo = DocumentRepository(session=session)
  department_repo = DepartmentRepository(session=session)
  chunk_repository = ChunkRepository(session=session)
  department_controller = DepartmentController()
  document_controller = DocumentController()
  

  department =  await department_repo.get_department_by_id(department_id=department_id)

  if file.content_type not in settings.SUPPORTED_CONTENT_TYPES:
     return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={
          'message': ResponseEnums.DOCUMENT_TYPE_IS_NOT_SUPPORTED.value
        }
      )

  if file.size > (settings.MAX_FILE_SIZE_IN_MB*1024*1024):
     return JSONResponse(
        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
        content={
          'message': ResponseEnums.DOCUMENT_LARGER_THAN_ALLOWED.value
        }
      )

  if  department==None:
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
          'message': ResponseEnums.DEPARTMENT_NOT_FOUND.value
        }
      )
  
  department_path =  department_controller.get_department_path(department_name=department.name)

  # validate do_reset 
    
  if do_reset == 1:
     # rm from document db
     await document_repo.delete_documents_by_department_id(departmet_id=department.id)

     await document_controller.remove_all_document_from_department(department_path=department_path)




     
  # insert into document
  
  document = await document_controller.create_document_object(file=file, department_id=department.id)
  insertion_status = await document_repo.insert_document(document)

  if not insertion_status:
     return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
          'messsage': ResponseEnums.DOCUMENT_ALREADY_EXIST.value
        }
      )
  # insert into storage
  await document_controller.upload_document_to_department_path(
    department_path=department_path,
    file=file
  )

  # insert into chunk , embeding
  doc_path = os.path.join(department_path,file.filename)
  chunk_controller = ChunckController(path=doc_path)
  chunks = chunk_controller.split_text(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
  chunk_objs = chunk_controller.make_chunk_object(
     chunks=chunks,
     department_id=department.id,
     document_id=document.id
  )
  chunks_inserted = await chunk_repository.insert_many_chunks(chunks=chunk_objs)

  embedding_service = EmbeddingService(
     session=session,
     document_id=document.id,
     Settings=settings,
     OpenAI_client=request.app.state.OpenAI_client
  )


  background_tasks.add_task(
     embedding_service.insert_embedings,
  )



  return JSONResponse(
    content={
      'messsage': ResponseEnums.DOCUMENT_UPLOADED_SUCCESSFULLY.value,
      'chunks_inserted': chunks_inserted
    }
  )



@router.get("/list/{departmet_id}")
async def list_docuemnts_in_deprtment(
  department_id: int ,
  session: AsyncSession = Depends(get_db_session)
):
  document_repo = DocumentRepository(session=session)

  documents= await document_repo.get_documents_by_department_id(departmet_id=department_id)

  documents_names =[
     doc.doc_name_id
     for doc in documents
  ]

  return JSONResponse(
      content={
          "message": documents_names
      }
  )




@router.delete("/delete/{document_id}")
async def delete_document(
   document_id: int,
   department_name: str,
   session: AsyncSession = Depends(get_db_session)
):
   
  document_repo = DocumentRepository(session=session)
  document_controller = DocumentController()

  document = await document_repo.get_document_by_id(document_id=document_id)

  _ = await document_repo.delete_document(document_id=document_id)
  _ = await document_controller.remove_document_from_storage(department_name=department_name, doc_name_id=document.doc_name_id)

  return JSONResponse(
    content={
        "message": ResponseEnums.DOCUMENT_DELETED_SUCCESSFULLY.value
    }
)

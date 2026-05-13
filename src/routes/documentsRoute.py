from fastapi import APIRouter, Depends,status, Request, UploadFile, File, Form
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
from models.db_schema.document import Document


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.post("/upload")
async def upload_document(
  request:Request,
  department_id:int = Form(...),
  file : UploadFile = File(...),
  session: AsyncSession = Depends(get_db_session),
  settings : Settings=  Depends(get_settings),
):

  document_repo = DocumentRepository(session=session)
  department_repo = DepartmentRepository(session=session)
  department_controller = DepartmentController()
  document_controller = DocumentController()

  department =  await department_repo.get_department_by_id(department_id=department_id)

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
  document = await document_controller.create_document_object(file=file, department_id=department.id)
  insertion_status = await document_repo.insert_document(document)

  if not insertion_status:
     return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
          'messsage': ResponseEnums.DOCUMENT_ALREADY_EXIST.value
        }
      )

  await document_controller.upload_document_to_department_path(
    department_path=department_path,
    file=file
  )


  return JSONResponse(
    content={
      'messsage': ResponseEnums.DOCUMENT_UPLOADED_SUCCESSFULLY.value
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
   session: AsyncSession = Depends(get_db_session)
):
   
  document_repo = DocumentRepository(session=session)

  _ = await document_repo.delete_document(document_id=document_id)
  
  return JSONResponse(
    content={
        "message": ResponseEnums.DOCUMENT_DELETED_SUCCESSFULLY.value
    }
)

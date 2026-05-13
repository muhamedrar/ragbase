from fastapi import APIRouter, Depends,status, Request, UploadFile, File, Form
import os
from pathlib import Path
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseEnums
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
import aiofiles
from controllers.department_controller import DepartmentController
from controllers.document_controller import DocumentController
from repositories.document_repository import  DocumentRepository
from repositories.department_repository import  DepartmentRepository



router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.post("/upload")
async def upload_document(
  department_id:int = Form(...),
  file : UploadFile = File(...),
  session: AsyncSession = Depends(get_db_session),
):

  document_repo = DocumentRepository(session=session)
  department_repo = DepartmentRepository(session=session)
  department_controller = DepartmentController()
  document_controller = DocumentController()

  department =  await department_repo.get_department_by_id(department_id=department_id)
  department_path =  department_controller.get_department_path(department_name=department.name)

  if not department_path:
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
          'message': ResponseEnums.DEPARTMENT_NOT_FOUND.value
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
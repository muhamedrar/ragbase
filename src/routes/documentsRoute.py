from fastapi import APIRouter, Depends,status, Request, UploadFile, File, Form
import os
from pathlib import Path
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseEnums
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session

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

 pass
from fastapi import APIRouter, Depends,status, Request
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


router.post("/upload/{department}")
async def upload_document(department: str, document_name: str):

 pass
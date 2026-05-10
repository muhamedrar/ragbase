from fastapi import APIRouter, Depends
from helpers.settings import get_settings


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


router.get("/upload/{department}")
async def upload_document(department: str, document_name: str):

 pass
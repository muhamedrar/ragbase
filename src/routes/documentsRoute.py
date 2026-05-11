from fastapi import APIRouter, Depends



router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


router.post("/upload/{department}")
async def upload_document(department: str, document_name: str):

 pass
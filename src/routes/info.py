from fastapi import APIRouter, Depends
from helpers.settings import get_settings


router = APIRouter(
    prefix="/info",
    tags=["info"]
    )

@router.get("/")
async def info(settings = Depends(get_settings)):
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION
    }





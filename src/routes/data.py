from fastapi import APIRouter, Depends
from helpers.settings import get_settings

settings = get_settings()
router = APIRouter(
    prefix="/data",
    tags=["data"]
    )

@router.get("/info")
async def info():
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION
    }





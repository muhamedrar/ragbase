from fastapi import APIRouter, Depends
from helpers.settings import get_settings


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)



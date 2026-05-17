from fastapi import APIRouter, Depends,status, Request, UploadFile, File, Form , BackgroundTasks
import os
from pathlib import Path
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseEnums
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from helpers.settings import Settings, get_settings
from services.GenerationModelService import GenerationModelService



router = APIRouter(
    prefix="/nlp/v1",
    tags=["nlp,v1"]
)



@router.get('/search')
async def search(
  request:Request,
  query:str  ,
  limit:int,
  session: AsyncSession = Depends(get_db_session),
  settings : Settings=  Depends(get_settings),
):
    gen_service = GenerationModelService(
        session=session,
        OpenAI_client=request.app.state.OpenAI_client,
        Settings=settings
    )


    result = await gen_service.search_vector_db(query=query,limit=limit)

    test_result = [
        {   'score' : row._mapping['score'],
            'content' :row._mapping['content']
        }
        for row in result
        
    ]

    return JSONResponse(
        content={"message" : test_result}
    )
    
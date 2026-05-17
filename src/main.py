from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.info import router as info_router
from routes.departmentRoute import router as department_router
from routes.documentsRoute import router as document_router
from routes.nlpRoute import router as nlp_router
from helpers.settings import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import logging
from openai import AsyncOpenAI

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_async_engine(
        url=settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    app.state.settings = settings
    logger.info(f"Starting {settings.APP_NAME} version {settings.APP_VERSION}")

    app.state.db_client = async_sessionmaker(
        bind=engine,
        expire_on_commit=False
    )
    logger.info(f"Started db_client")


    app.state.OpenAI_client= AsyncOpenAI(
        base_url=settings.OPENAI_URL,
        api_key=settings.OPENAI_TOKEN
    )
    logger.info(f"loading OpenAI_client")
    yield
    await engine.dispose()
    logger.info(f"Shutting down db_client")

    await app.state.OpenAI_client.close()
    logger.info(f"Shutting down OpenAI_client")


    logger.info(f"Shutdown complete for {settings.APP_NAME}")



app = FastAPI(lifespan=lifespan)

app.include_router(info_router)
app.include_router(department_router)
app.include_router(document_router)
app.include_router(nlp_router)
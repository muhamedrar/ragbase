from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.info import router as info_router
from helpers.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    
    app.state.settings = settings
    print(f"Starting {settings.APP_NAME} version {settings.APP_VERSION}")

    yield

    print(f"Shutting down {settings.APP_NAME}")


app = FastAPI(lifespan=lifespan)

app.include_router(info_router)
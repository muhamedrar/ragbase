from fastapi import FastAPI
from routes.info import router as info_router


app = FastAPI()

app.include_router(info_router)
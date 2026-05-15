from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
import os
from typing import List



BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = os.path.join(BASE_DIR,'.env')




class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path,env_file_encoding='utf-8')


    APP_NAME:str
    APP_VERSION:str
    
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_URL:str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str 

    DRIVER: str = "asyncpg"

    MAX_FILE_SIZE_IN_MB : int = 10
    SUPPORTED_CONTENT_TYPES: List[str]

    OPENAI_TOKEN=str
    OPENAI_URL=str
    OPENAI_GENERATION_MODEL=str
    OPENAI_EMBEDING_MODEL=str

    MODEL_DIMENSION_SIZE=int

    @property
    def DATABASE_URL(self) -> str:
        driver_part = f"+{self.DRIVER}" if self.DRIVER else ""
        
        return (
            f"postgresql{driver_part}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_URL}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


    
@lru_cache()
def get_settings():
    return Settings()

    
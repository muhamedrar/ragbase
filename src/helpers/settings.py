from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict('.env',env_file_encoding='utf-8',extra='ignore')


    APP_NAME:str
    APP_VERSION:str
    
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_URL:str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str 

    DRIVER: str = "psycopg2"

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

    
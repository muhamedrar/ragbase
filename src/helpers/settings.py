from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',env_file_encoding='utf-8')


    APP_NAME:str
    APP_VERSION:str
    
    POSTGERS_USER=str
    POSTGERS_PASSWORD=str
    POSTGERS_URL=str

    
@lru_cache()
def get_settings():
    return Settings()

    
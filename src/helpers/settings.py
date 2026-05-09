from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',env_file_encoding='utf-8')


    APP_NAME:str
    APP_VERSION:str

    
@lru_cache()
def get_settings():
    return Settings()

    
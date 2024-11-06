from os import environ
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file='.env', env_file_encoding='utf-8')
     
    TEST: Optional[bool] = False
    DATABASE_URL: Optional[str]
    
    TABLE_CACHE_DATA_ACCESS: Optional[str]
    TABLE_USERS: Optional[str]
    SECRET_KEY: Optional[str]
    ALGORITHM: Optional[str]
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int]
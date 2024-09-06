from os import environ
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file='.env', env_file_encoding='utf-8')
     
    TEST: Optional[bool] = False
    TABLE_CONTROL_LOG: Optional[str]
    DATABASE_URL: Optional[str]
    
        
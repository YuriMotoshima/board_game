from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file='.env', env_file_encoding='utf-8')
    
    UUID: str = Field(default_factory=lambda: uuid4().__str__())
    DATE_TIME: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d'T'%H:%M:%S.%f")[:-3])
    
    TEST: Optional[bool] = False
    DATABASE_URL: Optional[str]
    
    TABLE_CACHE_DATA_ACCESS: Optional[str]
    TABLE_USERS: Optional[str]
    TABLE_TOKEN_DATA: Optional[str]
    SECRET_KEY: Optional[str]
    ALGORITHM: Optional[str] = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 5
    REFRESH_TOKEN_EXPIRE_DAYS: Optional[int] = 1
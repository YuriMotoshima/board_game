from typing import List

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import _settings as Settings
from app.models.base_model import BaseModel


class CacheData(BaseModel):
    __tablename__ = f"{Settings.TABLE_CACHE_DATA_ACCESS}"

    path: Mapped[str] = mapped_column(nullable=True)
    user_language: Mapped[str] = mapped_column(nullable=True)
    user_agent: Mapped[str] = mapped_column(nullable=True)
    client_host: Mapped[str] = mapped_column(nullable=True)
    geolocation: Mapped[JSON] = mapped_column(JSON, nullable=True)
    headers: Mapped[JSON] = mapped_column(JSON, nullable=True)
    scopes: Mapped[JSON] = mapped_column(JSON, nullable=True)

    token_list: Mapped[List["TokenData"]] = relationship(back_populates="cache_data")

from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column, registry

from app import _settings as Settings
from app.models.base_model import BaseModel


class Users(BaseModel):
    __tablename__ = f"{Settings.TABLE_USERS}"
    
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=False, nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import _settings as Settings
from app.models.base_model import BaseModel


class TokenData(BaseModel):
    __tablename__ = f"{Settings.TABLE_TOKEN_DATA}"
    
    id_cache_data: Mapped[int] = mapped_column(ForeignKey('CacheData.id'), nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    user_email: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    message_execution: Mapped[str] = mapped_column(nullable=True)

    cache_data: Mapped["CacheData"] = relationship(back_populates="token_list")

from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_by: Mapped[str] = mapped_column(unique=False, server_default="System")
    created_at: Mapped[datetime] = mapped_column(unique=False, server_default=func.now())
    updated_by: Mapped[str] = mapped_column(unique=False, nullable=True, server_default="System")
    updated_at: Mapped[datetime] = mapped_column(unique=False, nullable=True, onupdate=func.now())
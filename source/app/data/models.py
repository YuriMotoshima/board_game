from datetime import UTC, date, datetime

from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlalchemy import func
from app.config.settings import Settings
from app.data.database import engine

Settings = Settings()

table_registry = registry()

@table_registry.mapped_as_dataclass
class Users:
    __tablename__ = f"{Settings.TABLE_USERS}"
    
    id : Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=False)
    nickname: Mapped[str] = mapped_column(unique=True)
    created_by: Mapped[str] = mapped_column(init=False, unique=False, server_default="System")
    created_at: Mapped[datetime] = mapped_column(init=False, unique=False, server_default=func.now())
    updated_by: Mapped[str] = mapped_column(init=False, unique=False)
    updated_at: Mapped[datetime] = mapped_column(init=False, unique=False)

@table_registry.mapped_as_dataclass
class CacheData:
    __tablename__ = f"{Settings.TABLE_CACHE_DATA_ACCESS}"
    
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    geolocation: Mapped[dict]
    user_agent: Mapped[str]
    client_host: Mapped[str]
    state_json: Mapped[dict]
    created_by: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, unique=False, server_default=func.now())
    updated_by: Mapped[str]
    updated_at: Mapped[datetime]


table_registry.metadata.create_all(engine, checkfirst=True)
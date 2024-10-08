from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column, registry

from app.config.settings import Settings

# Registro das tabelas no table_registry
table_registry = registry()

Settings = Settings()

# Modelos definidos usando o registry
@table_registry.mapped_as_dataclass
class Users:
    __tablename__ = f"{Settings.TABLE_USERS}"
    
    id : Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=False, nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_by: Mapped[str] = mapped_column(init=False, unique=False, server_default="System")
    created_at: Mapped[datetime] = mapped_column(init=False, unique=False, server_default=func.now())
    updated_by: Mapped[str] = mapped_column(init=False, unique=False, nullable=True, server_default="System")
    updated_at: Mapped[datetime] = mapped_column(init=False, unique=False, nullable=True, onupdate=func.now())


@table_registry.mapped_as_dataclass
class CacheData:
    __tablename__ = f"{Settings.TABLE_CACHE_DATA_ACCESS}"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(nullable=True)
    user_language: Mapped[str] = mapped_column(nullable=True)
    user_agent: Mapped[str] = mapped_column(nullable=True)
    client_host: Mapped[str] = mapped_column(nullable=True)
    geolocation: Mapped[JSON] = mapped_column(JSON, nullable=True)
    headers: Mapped[JSON] = mapped_column(JSON, nullable=True)
    scopes: Mapped[JSON] = mapped_column(JSON, nullable=True)
    created_by: Mapped[str] = mapped_column(init=False, unique=False, server_default="System")
    created_at: Mapped[datetime] = mapped_column(init=False, unique=False, server_default=func.now())
    updated_by: Mapped[str] = mapped_column(init=False, unique=False, nullable=True, server_default="System")
    updated_at: Mapped[datetime] = mapped_column(init=False, unique=False, nullable=True, onupdate=func.now())

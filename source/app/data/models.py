from datetime import UTC, date, datetime

from sqlalchemy.orm import Mapped, mapped_column, registry

from app.config.settings import SETTINGS as Settings
from app.data.database import engine

table_registry = registry()

@table_registry.mapped_as_dataclass
class LogItem:
    __tablename__ = f"{Settings.TABLE_CONTROL_LOG}"
    
    request_id: Mapped[str] = mapped_column(primary_key=True)
    request_payload: Mapped[str] = mapped_column(nullable=False)
    request_headers: Mapped[str] = mapped_column(nullable=False)
    response_status_code: Mapped[int] = mapped_column(nullable=False)
    response_payload: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(UTC))
    tenant: Mapped[int] = mapped_column(default=None, nullable=True)
    roles_scope: Mapped[str] = mapped_column(default=None, nullable=True)
    partial_token: Mapped[str] = mapped_column(default=None, nullable=True)



table_registry.metadata.create_all(engine, checkfirst=True)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession

from app.config.settings import SETTINGS as settings

if settings.TESTS:
    engine = create_engine('sqlite:///:memory:')
else:
    engine= create_engine(settings.DATABASE_URL)

def get_session():
    with SQLAlchemySession(engine) as session:
        yield session
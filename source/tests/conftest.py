import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.app import app
from app.data.database import get_session
from app.data.models import table_registry
from tests.mocks.factories import UsersFactory


@pytest.fixture()
def client_app(session):
    """client_app up instance fastapi

    Args:
        session (engine): Connetion SqlAlchemy of test
    """
    def get_session_override():
        return session
    
    with TestClient(app) as client:
        # Set dependency in application fastapi
        app.dependency_overrides[get_session] = get_session_override
        yield client
        
    app.dependency_overrides.clear()
    

@pytest.fixture()
async def session():
    """session Create session to database on memory to tests
    """
    # Criação do engine assíncrono
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Criação das tabelas de forma assíncrona
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    # Criação da sessão assíncrona
    async with async_session() as session:
        yield session

    # Remoção das tabelas de forma assíncrona
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
        
        
@pytest.fixture()
async def add_user_to_db(session):
    async def _add_user_to_db(**kwargs):
        user = UsersFactory.build(**kwargs)
        try:
            session.add(user)
            await session.commit()
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            raise
        return user
    return _add_user_to_db



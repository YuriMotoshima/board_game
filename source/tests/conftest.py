import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import _settings as Settings
from app.app import app
from app.data.database import get_session
from app.models.base_model import BaseModel
from tests.mocks.factories import UsersFactory


@pytest.fixture()
def settings():
    return Settings()
    
    
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
    

@pytest.fixture
async def client_app_async(session):
    """client_app up instance fastapi

    Args:
        session (engine): Connetion SqlAlchemy of test
    """
    def get_session_override():
        return session

    # Override da dependência do banco de dados
    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(app=app, base_url="http://test") as client:
    # async with AsyncClient(app=app) as client:
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
        await conn.run_sync(BaseModel.metadata.create_all)

    # Criação da sessão assíncrona
    async with async_session() as session:
        yield session

    # Remoção das tabelas de forma assíncrona
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        
        
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



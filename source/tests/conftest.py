import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import _settings as Settings
from app.app import app
from app.data.database import get_session
from app.models.base_model import BaseModel
from tests.mocks.factories import (UsersFactory, CacheDataFactory, TokenDataFactory)


@pytest.fixture()
def settings():
    return Settings
    
    
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

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
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


@pytest.fixture()
async def add_cache_data(session):
    async def _add_cache_data(**kwargs):
        cache = CacheDataFactory.build(**kwargs)
        try:
            session.add(cache)
            await session.commit()
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            raise
        return cache
    return _add_cache_data


@pytest.fixture()
async def add_user_to_db(session):
    async def _add_user_to_db(**kwargs):
        user = UsersFactory.build(**kwargs)
        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)  # garante que volta com ID preenchido
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            raise
        return user
    return _add_user_to_db


@pytest.fixture()
async def add_cache_data(session):
    async def _add_cache_data(**kwargs):
        cache = CacheDataFactory.build(**kwargs)
        try:
            session.add(cache)
            await session.commit()
            await session.refresh(cache)
        except Exception as e:
            print(f"Erro ao adicionar cache: {e}")
            raise
        return cache
    return _add_cache_data


@pytest.fixture()
async def add_token_data(session, add_cache_data):
    async def _add_token_data(**kwargs):
        # Se não passar id_cache_data, cria um novo CacheData
        id_cache_data = kwargs.get('id_cache_data')
        if not id_cache_data:
            cache = await add_cache_data()
            id_cache_data = cache.id

        # Atualiza o kwargs para passar o id_cache_data correto
        kwargs['id_cache_data'] = id_cache_data

        token_data = TokenDataFactory.build(**kwargs)
        try:
            session.add(token_data)
            await session.commit()
            await session.refresh(token_data)
        except Exception as e:
            print(f"Erro ao adicionar token_data: {e}")
            raise
        return token_data
    return _add_token_data

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.app import app
from app.data.models import table_registry


@pytest.fixture()
def client_app():
    return TestClient(app)


@pytest.fixture()
async def session():
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
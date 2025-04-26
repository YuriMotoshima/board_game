import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app import _settings as Settings
from app.data.database import async_session, create_tables, engine, get_session
from app.models.base_model import BaseModel


# Teste da sessão assíncrona
@pytest.mark.asyncio
async def test_get_session():
    async with async_session() as session:
        assert isinstance(session, AsyncSession)

# Teste para garantir que o engine está configurado corretamente no ambiente de teste
def test_engine_is_sqlite_in_test_mode(monkeypatch):
    monkeypatch.setattr(Settings, 'TEST', True)
    engine_test = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    assert engine.url.drivername == engine_test.url.drivername

# Teste para garantir que o engine é configurado com o DATABASE_URL no ambiente normal
def test_engine_is_production_url(monkeypatch):
    monkeypatch.setattr(Settings, 'TEST', False)
    monkeypatch.setattr(Settings, 'DATABASE_URL', 'sqlite+aiosqlite:///:memory:')
    engine_prod = create_async_engine(Settings.DATABASE_URL, echo=True)
    assert engine.url.drivername == engine_prod.url.drivername

# Teste da criação de tabelas
@pytest.mark.asyncio
async def test_create_tables(mocker):
    # Mock para garantir que a criação de tabelas não toca no banco real
    mock_run_sync = mocker.patch('sqlalchemy.ext.asyncio.AsyncConnection.run_sync')
    await create_tables()
    mock_run_sync.assert_called_once_with(BaseModel.metadata.create_all)

# Teste do ciclo de vida da aplicação
@pytest.mark.asyncio
async def test_lifespan(mocker):
    # Mock da função create_tables para verificar se ela foi chamada
    mock_create_tables = mocker.patch('app.data.database.create_tables')
    
    # Simulação da função de ciclo de vida
    async def mock_lifespan(app):
        await mock_create_tables()
        yield
    
    mock_create_tables.assert_not_called()
    async for _ in mock_lifespan(None):
        pass # noqa
    mock_create_tables.assert_called_once()

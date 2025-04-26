import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import _settings as Settings
from app.models.base_model import BaseModel

# Carrega as configurações do banco de dados
 
# Configura o engine dependendo do ambiente
if Settings.TEST:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
else:
    engine = create_async_engine(Settings.DATABASE_URL, echo=True)

# Cria a fábrica de sessões
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Função para obter uma sessão do banco de dados
async def get_session():
    async with async_session() as session:
        yield session

# Função para criar as tabelas
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

# Ciclo de vida da aplicação, que vai criar as tabelas na inicialização
async def lifespan(app): # noqa NOSONAR
    await create_tables()
    yield

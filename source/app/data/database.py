import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import Settings
from app.data.models import table_registry  # Importamos apenas o registry dos modelos

# Carrega as configurações do banco de dados
Settings = Settings()

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
    metadata = table_registry.metadata
    async with engine.begin() as conn:
        # Verifica e loga tabelas existentes
        existing_tables = await conn.run_sync(lambda conn: list(metadata.tables.keys()))
        logging.info(f"Existing tables: {existing_tables}")
        
        # Cria as tabelas, se não existirem
        if not existing_tables:
            await conn.run_sync(metadata.create_all)
            logging.info("Tables created successfully.")
        else:
            logging.info("Tables already exist, skipping creation.")

# Ciclo de vida da aplicação, que vai criar as tabelas na inicialização
async def lifespan(app):
    await create_tables()
    yield

# Usar uma imagem base Python
FROM python:3.11-slim

# Definir variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Criar e definir o diretório de trabalho
WORKDIR /source

# Copiar todos os arquivos da aplicação para o diretório de trabalho
COPY ./source/ /source/

# Copiar os arquivos de configuração do Poetry
# COPY ./source/pyproject.toml /source

# Instalar as dependências usando Poetry
RUN pip install --upgrade pip
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN set -e; \
    poetry run pytest --cov=app --cov-report=xml --disable-warnings; \
    COVERAGE_RESULT=$(coverage report --fail-under=79); \
    if [ $? -ne 0 ]; then \
        echo "$COVERAGE_RESULT"; \
        exit 1; \
    fi

# Remover as dependências de desenvolvimento
RUN poetry remove pytest pytest-cov isort factory-boy pytest-httpx pytest-mock

# Definir o usuário não privilegiado para execução da aplicação
RUN useradd -m appuser
USER appuser

# Expor a porta da aplicação
EXPOSE 8080

# Comando para executar a aplicação
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]

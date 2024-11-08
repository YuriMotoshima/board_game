## Structure

```sh
tree /f /a > estrutura_diretorios.txt


.source\
|   .coverage
|   .dockerignore
|   .env
|   database.db
|   Dockerfile
|   estrutura_diretorios.txt
|   poetry.lock
|   pyproject.toml
|   README.md
|   
+---.pytest_cache
|   |   .gitignore
|   |   CACHEDIR.TAG
|   |   README.md
|   |   
|   \---v
|       \---cache
|               lastfailed
|               nodeids
|               stepwise
|               
+---.vscode
|       launch.json
|       settings.json
|       
+---app
|   |   app.py
|   |   __init__.py
|   |   
|   +---config
|   |       collections_exceptions.py
|   |       log.py
|   |       settings.py
|   |       
|   +---data
|   |       database.py
|   |       models.py
|   |       
|   +---middleware
|   |       middle.py
|   |       
|   +---modules
|   |       db_tools.py
|   |       
|   +---routers
|   |       jwt_security.py
|   |       users.py
|   |       
|   +---schemas
|   |       schemas_jwt.py
|   |       schemas_users.py
|   |       
|   \---security
|           security.py
|           
\---tests
    |   conftest.py
    |   __init__.py
    |   
    +---mocks
    |       factories.py
    |       
    +---tests_app
    |       test_app.py
    |       
    +---tests_config
    |       test_exceptions.py
    |       test_logs.py
    |       
    +---tests_database
    |       test_db.py
    |       
    +---tests_middleware
    |       test_middleware.py
    |       
    +---tests_modules
    |       test_db_tools.py
    |       
    +---tests_routers
    |       test_jwt_security.py
    |       test_users.py
    |       
    \---tests_security
            test_security.py
```

<br>

# PyProject
### Collection and Configuration

```sh
python = "^3.11"
uvicorn = "^0.30.6"
fastapi = "^0.113.0"
sqlalchemy = {extras = ["aiomysql", "asyncpg"], version = "^2.0.34"}
pydantic = {extras = ["email"], version = "^2.9.1"}
pydantic-settings = "^2.4.0"
geocoder = "^1.38.1"
pwdlib = {extras = ["argon2"], version = "^0.2.1"}
httpx = "^0.27.2"
pyjwt = "^2.9.0"
python-multipart = "^0.0.17"
asyncpg = "^0.29.0"
aiomysql = "^0.2.0"
```
## Default
`python` - Define a versão do Python usada no projeto.<br>
`uvicorn` - Servidor ASGI assíncrono para rodar aplicações web (ex. FastAPI).<br>
`fastapi` - Framework web moderno e rápido, usado para criar APIs e rotas.<br>
`sqlalchemy` - ORM para interagir com bancos de dados de maneira Pythonica.<br>
`pydantic` - Validação e padronização de estruturas de dados em Python.<br>
`pydantic-settings` - Facilita o uso e validação de variáveis de ambiente no Pydantic.<br>

## Tools
`geocoder` - Obtém geolocalização (latitude/longitude) com base no IP.<br>
`pwdlib` - Biblioteca para gerenciamento e validação de senhas.<br>
`httpx` - Cliente HTTP assíncrono para fazer requisições web.<br>

## Security
`pyjwt` - Trabalha com JSON Web Tokens (JWT) para autenticação e autorização.<br>
`python-multipart` - Processa uploads de arquivos e dados multipart/form-data.<br>

## Async
`asyncpg` - Driver assíncrono de alta performance para PostgreSQL.<br>
`aiomysql` - Driver assíncrono para MySQL/MariaDB.<br>

<br>

# PyProject Dev Dependencies
### Collection and Configuration

```sh
[tool.poetry.group.dev.dependencies]
taskipy = "^1.13.0"
pytest = "^8.3.2"
isort = "^5.13.2"
pytest-cov = "^5.0.0"
aiosqlite = "^0.20.0"
asyncpg = "^0.29.0"
aiomysql = "^0.2.0"
sqlalchemy = {extras = ["aiomysql", "asyncpg"], version = "^2.0.34"}
pytest-asyncio = "^0.24.0"
factory-boy = "^3.3.1"
gevent = "^24.10.3"
```

## CLI
`taskipy` - Executa comandos de terminal (CLI), veja lista de comando em [tool.taskipy.tasks]<br>

## Tests
`pytest` - Lib de tests<br>
`pytest-cov` - Lib para fazer cobertura dos tests<br>
`pytest-asyncio` - Lib para fazer test asyncronos<br>
`factory-boy` - Lib para criar dados fake<br>
`gevent` - Lib auxiliar que ajuda o coverage conseguir seguir os testes e fazer a cobertura <br>correta, ele manipula as thread de execução para que o coverage não se perca

## Tools
`isort` - Lib para organizar os imports no codigo<br>
`aiosqlite` - Lib para rodar o sqlite em teste na memoria<br>

<br>

# PyProject Personal Configurations

```sh
[tool.coverage.poetry]
enabled = true

[tool.pytest.ini_options]
asyncio_mode = "auto"

[tool.coverage.report]
show_missing = true
fail_under = 80  # Pode ajustar conforme o nível desejado de cobertura mínima
skip_covered = true  # Isso evitará mostrar linhas já cobertas

[tool.coverage.run]
concurrency = ["gevent"]
source = ["app"]
omit = [
    "config/*",
    "images/*",
    "*/__init__.py",
]

[tool.taskipy.tasks]
test = 'pytest -s -x --cov=app -vv'
post_test = 'coverage html'
clear = "isort . && powershell -Command \"Get-ChildItem -Path . -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force; Get-ChildItem -Path . -Recurse -Directory -Filter 'logs' | Remove-Item -Recurse -Force; Get-ChildItem -Path . -Recurse -Directory -Filter 'htmlcov' | Remove-Item -Recurse -Force\""
``` 

## [tool.coverage.poetry]
`enabled = true` - Ativa o plugin do Poetry para trabalhar com coverage, que mede a <br>cobertura de testes no código.

## [tool.pytest.ini_options]
`asyncio_mode = "auto"` - Configura o Pytest para lidar automaticamente com testes <br>assíncronos usando asyncio.

## [tool.coverage.report]
`show_missing = true` - Mostra as linhas de código que não foram cobertas pelos testes.<br>
`fail_under = 80` - Falha se a cobertura de testes estiver abaixo de 80%.<br>
`skip_covered = true` - Oculta as linhas de código que já foram totalmente cobertas pelos testes.<br>

## [tool.coverage.run]
`concurrency = ["gevent"]` - Configura o coverage para lidar com código concorrente usando gevent.<br>
`source = ["app"]` - Define que o coverage deve medir a cobertura apenas no diretório app.<br>
`omit` - Omitir arquivos ou padrões específicos durante a execução do coverage (vazio aqui, <br>mas pode ser usado para excluir arquivos da análise).

## [tool.coverage.poetry]

`test` - Atalho (CLI) para executar um comando no terminal que roda o test<br>
`post_test` - Atalho (CLI) para executar um comando no terminal que roda a coberto em html<br>
`clear` - Atalho (CLI) para executar um comando no terminal que remove pastas e organizar os imports <br>
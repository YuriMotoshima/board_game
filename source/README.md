tree /F > estrutura_diretorios.txt

```sh
.source\
│   .coverage
│   .dockerignore
│   .env
│   database.db
│   Dockerfile
│   estrutura_diretorios.txt
│   poetry.lock
│   pyproject.toml
│   README.md
│   
├───app
│   │   app.py
│   │   __init__.py
│   │   
│   ├───config
│   │       collections_exceptions.py
│   │       log.py
│   │       settings.py
│   │       
│   ├───data
│   │       database.py
│   │       models.py
│   │       
│   ├───middleware
│   │       middle.py
│   │       
│   ├───modules
│   │       db_tools.py
│   │       
│   ├───routers
│   │       users.py
│   │       
│   ├───schemas
│   │       schemas_users.py
│   │       
│   └───security
│           security.py
│           
├───logs
│   └───13-10-2024
│           [DEV] Logs - 13-10-2024 12.log
│           [DEV] Logs - 13-10-2024 16.log
│           [DEV] Logs - 13-10-2024 22.log
│           
└───tests
    │   conftest.py
    │   __init__.py
    │   
    ├───mocks
    │       factories.py
    │       
    ├───tests_app
    │       test_app.py
    │       
    ├───tests_config
    │       test_exceptions.py
    │       test_logs.py
    │       
    ├───tests_database
    │       test_db.py
    │       
    ├───tests_middleware
    │       test_middleware.py
    │       
    ├───tests_modules
    │       test_db_tools.py
    │       
    └───tests_routers
            test_users.py
```
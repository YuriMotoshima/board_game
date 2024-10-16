tree /F > estrutura_diretorios.txt

```sh
.source\
ª   .coverage
ª   .dockerignore
ª   .env
ª   database.db
ª   Dockerfile
ª   estrutura_diretorios.txt
ª   poetry.lock
ª   pyproject.toml
ª   
+---.pytest_cache
ª   ª   .gitignore
ª   ª   CACHEDIR.TAG
ª   ª   README.md
ª   ª   
ª   +---v
ª       +---cache
ª               stepwise
ª               
+---.vscode
ª       launch.json
ª       settings.json
ª       
+---app
ª   ª   app.py
ª   ª   __init__.py
ª   ª   
ª   +---config
ª   ª       collections_exceptions.py
ª   ª       log.py
ª   ª       settings.py
ª   ª       
ª   +---data
ª   ª       database.py
ª   ª       models.py
ª   ª       
ª   +---middleware
ª   ª       middle.py
ª   ª       
ª   +---modules
ª   ª       db_tools.py
ª   ª       
ª   +---routers
ª   ª       users.py
ª   ª       
ª   +---schemas
ª   ª       schemas_users.py
ª   ª       
ª   +---security
ª           security.py
ª           
+---tests
    ª   conftest.py
    ª   __init__.py
    ª   
    +---mocks
    ª       factories.py
    ª       
    +---tests_config
    ª       test_exceptions.py
    ª       test_logs.py
    ª       
    +---tests_database
    ª       test_db.py
    ª       
    +---tests_middleware
    ª       test_middleware.py
    ª       
    +---tests_modules
    ª       test_db_tools.py
    ª       
    +---tests_routers
            test_users.py
            

```
from http import HTTPStatus

from fastapi import FastAPI, Request

from app.data.database import lifespan
from app.middleware.middle import HeaderValidationMiddleware
from app.routers import jwt_security, users
from app.schemas.schemas_users import SchemaMessage

# Inicializa a aplicação FastAPI com o ciclo de vida definido
app = FastAPI(lifespan=lifespan)

# Inclui o router de usuários
app.include_router(users.router)
app.include_router(jwt_security.router)

# Adiciona o middleware de validação de headers
app.add_middleware(HeaderValidationMiddleware)

# Rota simples para teste
@app.get('/', status_code=HTTPStatus.OK, response_model=SchemaMessage)
def read_root(request: Request):
    return {'message': 'Olá mundo', 'headers': request.headers, 'scope': str(request.scope), 'state': request.state._state}

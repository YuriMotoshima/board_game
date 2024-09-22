from http import HTTPStatus

from fastapi import FastAPI, Request

from app.data.database import lifespan  # Agora o lifespan vem de database.py
from app.data.schemas import SchemaMessage
from app.middleware.middle import HeaderValidationMiddleware
from app.routers import users

# Inicializa a aplicação FastAPI com o ciclo de vida definido
app = FastAPI(lifespan=lifespan)

# Inclui o router de usuários
app.include_router(users.router)

# Adiciona o middleware de validação de headers
app.add_middleware(HeaderValidationMiddleware)

# Rota simples para teste
@app.get('/', status_code=HTTPStatus.OK, response_model=SchemaMessage)
def read_root(request: Request):
    return {'message': 'Olá mundo', 'headers': request.headers, 'scope': str(request.scope), 'state': request.state._state}

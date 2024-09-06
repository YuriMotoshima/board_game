from http import HTTPStatus

from fastapi import FastAPI, Request
from app.data.schemas import Message
from app.middleware.security import HeaderValidationMiddleware
app = FastAPI()


# Adicione o middleware antes de incluir as rotas
app.add_middleware(HeaderValidationMiddleware)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root(request:Request):
    return {'message':'Olá mundo', 'headers':request.headers, 'scope': str(request.scope), 'state':request.state._state}

from http import HTTPStatus

from fastapi import FastAPI, Request
from app.data.schemas import Message

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root(request:Request):
    return {'message':'Olá mundo', 'headers':request.headers, 'scope': str(request.scope)}
    
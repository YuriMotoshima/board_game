from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.config.collections_exceptions import collections_exceptions
from app.data.database import get_session
from app.data.models import Users
from app.modules.db_tools import _send_to_data
from app.schemas.schemas_jwt import Token
from app.security.security import create_access_token, verify_password

db_session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/token', tags=['Token'])


@router.post('/get_token', status_code=HTTPStatus.OK, response_model=Token)
async def create_token(session: db_session, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await session.scalar(select(Users).where(Users.nickname == form_data.username))

    if not user or not verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas.")
    
    access_token = create_access_token(data={"sub":user.email})
    
    return {'access_token': access_token, 'token_type':'Bearer'}
    
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from app.config.collections_exceptions import collections_exceptions
from app.data.database import get_session
from app.models import CacheData, TokenData, Users
from app.modules.db_tools import _send_to_data
from app.schemas.schemas_jwt import RefreshTokenPayload, Token
from app.security.security import (create_access_token, decode_refresh_token,
                                   verify_password)

db_session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/token', tags=['Token'])


@router.post('/get_token', status_code=HTTPStatus.OK, response_model=Token)
async def create_token(request: Request, session: db_session, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await session.scalar(select(Users).where(Users.nickname == form_data.username))

    if not user or not verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas.")
    
    token_dict = create_access_token(data={"sub": user.email})

    token_log = TokenData(
        id_cache_data=request.state.cache_data['id'],
        user_name=user.nickname,
        user_email=user.email,
        access_token=token_dict["access_token"],
        refresh_token=token_dict["refresh_token"],
        message_execution="Token gerado com sucesso."
    )
    await _send_to_data(db_class=token_log, session=session)

    return token_dict


@router.post('/get_refresh', status_code=HTTPStatus.OK, response_model=Token)
async def create_refresh_token(
    request: Request,
    session: db_session,
    payload: RefreshTokenPayload
):
    try:

        decode_refresh = decode_refresh_token(refresh_token=payload.refresh_token)

        result = await session.execute(
            select(TokenData)
            .join(TokenData.cache_data) 
            .options(joinedload(TokenData.cache_data))
            .where(and_(TokenData.refresh_token == payload.refresh_token, CacheData.path == '/token/get_token'))
        )

        search_token = result.scalar_one_or_none()
        
        if not search_token.cache_data:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Cache não encontrado")
        
        # 1. Validação User-Agent
        if search_token.cache_data.user_agent != request.state.user_agent:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.value[1])

        # 2. Validação IP
        if search_token.cache_data.client_host != request.state.client_host:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.value[1])

        # 3. Validação de país (opcional)
        if search_token.cache_data.geolocation.get("country") != request.state.geolocation.get("country"):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.value[1])
        
        # 3. Validação email (opcional)
        if search_token.user_email != decode_refresh['sub']:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.value[1])

        # Gera novo par de tokens
        new_tokens = create_access_token(data={"sub": decode_refresh['sub']})

        # Pega o usuário para registrar no TokenData
        user = await session.scalar(select(Users).where(Users.email == decode_refresh['sub']))
        if not user:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.value[1])

        # Salva no banco (TokenData ou outro log de emissão)
        token_data = TokenData(
            id_cache_data=search_token.cache_data.id,
            user_name=user.nickname,
            user_email=user.email,
            access_token=new_tokens['access_token'],
            refresh_token=new_tokens['refresh_token'],
            message_execution='refresh_token issued'
        )
        await _send_to_data(db_class=token_data, session=session)

        return new_tokens

    except ExpiredSignatureError as err:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Signature has expired')

    except Exception as err:
        collections_exceptions(err)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Erro ao gerar novo token")

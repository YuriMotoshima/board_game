from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.data.database import get_session
from app.data.models import Users
from app.data.schemas import (SchemaPatchUser, SchemaPutUser,
                              SchemaResponseUsers, SchemaUsers)

db_session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', status_code=HTTPStatus.OK, response_model=List[SchemaResponseUsers])
async def get_users(session:db_session, limit: int = 10 , offset:int = 0):
    result = await session.scalars(
        select(Users).limit(limit).offset(offset)
    )
    return result


@router.post('/', status_code=HTTPStatus.CREATED, response_model=SchemaResponseUsers)
async def create_user(user:SchemaUsers, session:db_session):
    db_user = await session.scalar(
        select(Users).where(Users.email == user.email)
    )
    if db_user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail='Users exists.') 
    
    db_user = (Users(**user.model_dump()))
    session.add(db_user)
    await session.commit()
    session.refresh(db_user)
    
    return db_user


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def get_user(user:SchemaUsers, user_id:int, session:db_session):
    db_user = await session.scalar(
        select(Users).where(Users.id == user_id)
    )
    if not db_user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail='User not found.') 
    
    session.refresh(db_user)
    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def update_user(user_id: int, user: SchemaPutUser, session: db_session):
    db_user = await session.scalar(select(Users).where(Users.id == user_id))
    
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    
    # Atualiza todos os campos do recurso
    db_user.name = user.name
    db_user.email = user.email
    db_user.nickname = user.nickname
    db_user.password = user.password
    db_user.updated_by = "System"  # ou o usuário que está fazendo a atualização
    
    await session.commit()
    session.refresh(db_user)
    
    return db_user


@router.patch('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def partial_update_user(user_id: int, user: SchemaPatchUser, session: db_session):
    db_user = await session.scalar(select(Users).where(Users.id == user_id))
    
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    
    # Atualiza apenas os campos que foram passados no PATCH
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    if user.nickname is not None:
        db_user.nickname = user.nickname
    if user.password is not None:
        db_user.password = user.password
    
    db_user.updated_by = "System"  # ou o usuário que está fazendo a atualização
    
    await session.commit()
    session.refresh(db_user)
    
    return db_user

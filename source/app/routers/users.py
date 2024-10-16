from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.config.collections_exceptions import collections_exceptions
from app.data.database import get_session
from app.data.models import Users
from app.modules.db_tools import _send_to_data
from app.schemas.schemas_users import (SchemaPatchUser, SchemaPutUser,
                                       SchemaPutUserPassword,
                                       SchemaResponseUsers, SchemaUsers)
from app.security.security import verify_password

db_session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', status_code=HTTPStatus.OK, response_model=List[SchemaResponseUsers])
async def get_users(session:db_session,
                    limit: int = Query(10, gt=0, le=20, description="Limit must be between 1 and 20"), 
                    offset: int = Query(0, ge=0, description="Offset must be 0 or greater")
                    ):
    result = await session.scalars(
        select(Users).limit(limit).offset(offset)
    )
    return result


@router.post('/', status_code=HTTPStatus.CREATED, response_model=SchemaResponseUsers)
async def create_user(user: SchemaUsers, session: db_session):
    try:
        # Verificando se o email ou o nickname já estão em uso
        db_user = await session.scalar(
            select(Users).where(
                or_(Users.email == user.email, Users.nickname == user.nickname)
            )
        )

        if db_user:
            if db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, 
                    detail='Email is already in use.'
                )
            elif db_user.nickname == user.nickname:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, 
                    detail='Nickname is already in use.'
                )
        
        db_user = Users(**user.model_dump())
        return await _send_to_data(db_class=db_user, session=session)
    
    except HTTPException as http_err:
        # Propaga a exceção HTTP corretamente para o cliente.
        raise http_err
    
    except Exception as err:
        collections_exceptions(err)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
            detail="An unexpected error occurred, verify logs the application."
        )


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def get_user(user_id:int, session:db_session):
    db_user = await session.scalar(
        select(Users).where(Users.id == user_id)
    )
    if not db_user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail='User not found.') 
    
    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def update_user(user_id: int, user: SchemaPutUser, session: db_session):
    db_user = await session.scalar(select(Users).where(Users.id == user_id))
    
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
        
    return await _send_to_data(db_class=db_user, session=session)


@router.patch('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def partial_update_user(user_id: int, user: SchemaPatchUser, session: db_session):
    db_user = await session.scalar(select(Users).where(Users.id == user_id))
    
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    return await _send_to_data(db_class=db_user, session=session)


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=SchemaResponseUsers)
async def update_user_password(user_id: int, user: SchemaPutUserPassword, session: db_session):
    db_user = await session.scalar(select(Users).where(and_(Users.id == user_id, Users.email == user.email)))
    
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    
    if not verify_password(plain_password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Verify the last password.")
    
    db_user.password = user.new_password
    
    return await _send_to_data(db_class=db_user, session=session)

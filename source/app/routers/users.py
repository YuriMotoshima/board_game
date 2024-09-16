from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data.schemas import SchemaUsers, SchemaResponseUsers
from app.data.models import Users
from app.data.database import get_session
from sqlalchemy.future import select
 
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
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data.schemas import SchemaUsers
from app.data.models import Users
from app.data.database import get_session
from sqlalchemy.future import select

db_session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/users', tags=['Users'])

router.get('/', status_code=HTTPStatus.OK, response_model=List[SchemaUsers])
async def get_users(users:Users, session:db_session):
    result = await session.execute(select(users))
    users = result.scalars().all()
    return users
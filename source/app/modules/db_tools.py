from http import HTTPStatus
from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedAsDataclass

DBModels = TypeVar('TDBModels', bound=MappedAsDataclass)

async def _send_to_data(db_class: DBModels, session: AsyncSession) -> DBModels:
    if not db_class:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
            detail='An error occurred while creating the record.'
        )
        
    try:
        session.add(db_class)
        await session.commit()
        await session.refresh(db_class)
        
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail=f"Integrity error: {str(e)}"
        )
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    return db_class

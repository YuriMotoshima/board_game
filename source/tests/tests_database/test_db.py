
import pytest
from sqlalchemy import select

from app.models.CacheData import Users


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = Users(email="joao.silva@tests.com", name="Joao Silva", nickname="SilvaJ", password="Teste@123")
    session.add(new_user)
    await session.commit()
    
    user = await session.scalar(select(Users).where(Users.nickname == "SilvaJ"))
    
    assert user.name == "Joao Silva"
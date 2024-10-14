import factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import Users
from app.security.security import get_password_hash


class UsersFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Users
        sqlalchemy_session = AsyncSession
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker('email')
    name = factory.Faker('name')
    nickname = factory.Faker('user_name')
    password = password=factory.Faker('password')

import factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.CacheData import Users
from app.security.security import get_password_hash


class UsersFactory(factory.Factory):
    class Meta:
        model = Users

    email = factory.Faker('email')
    name = factory.Faker('name')
    nickname = factory.Faker('user_name')
    password = password=factory.Faker('password')

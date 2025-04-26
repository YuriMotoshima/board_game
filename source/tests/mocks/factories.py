import factory

from app.models import Users


class UsersFactory(factory.Factory):
    class Meta:
        model = Users

    email = factory.Faker('email')
    name = factory.Faker('name')
    nickname = factory.Faker('user_name')
    password = password=factory.Faker('password')

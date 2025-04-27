import factory

from app.models import Users, CacheData, TokenData


class UsersFactory(factory.Factory):
    class Meta:
        model = Users

    email = factory.Faker('email')
    name = factory.Faker('name')
    nickname = factory.Faker('user_name')
    password = password=factory.Faker('password')


class CacheDataFactory(factory.Factory):
    class Meta:
        model = CacheData
        
    path = factory.Faker('uri_path')
    user_language = factory.Faker('language_code')
    user_agent = factory.Faker('user_agent')
    client_host = factory.Faker('ipv4')
    geolocation = factory.LazyFunction( lambda: {"country": factory.fake.country_code(), "city": factory.fake.city()} )
    headers = factory.LazyFunction( lambda: {"Content-Type": "application/json", "Accept-Language": factory.fake.language_code()} )
    scopes = factory.LazyFunction( lambda: ["read", "write"] )
    

class TokenDataFactory(factory.Factory):
    class Meta:
        model = TokenData

    cache_data = factory.SubFactory(CacheDataFactory)
    id_cache_data = factory.LazyAttribute(lambda _: 1)
    user_name = factory.Faker('user_name')
    user_email = factory.Faker('email')
    access_token = factory.Faker('uuid4')
    refresh_token = factory.Faker('uuid4')
    message_execution = factory.Faker('sentence')
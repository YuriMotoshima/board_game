import pytest

from app.schemas.schemas_users import SchemaUsers


@pytest.mark.asyncio
async def test_get_app(client_app):
    """test_get_app

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get('/')
    assert response.status_code == 200


# Users
@pytest.mark.asyncio
async def test_get_users_success(client_app):
    """test_get_users_success

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get('/users/?limit=10&offset=0')
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Verifica se a estrutura da resposta corresponde ao modelo esperado (schema de usuários)
    for user in response.json():
        assert "id" in user
        assert "name" in user


@pytest.mark.asyncio
async def test_get_users_sql_injection_in_limit(client_app):
    """test_get_users_sql_injection_in_limit

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=1;DROP TABLE users;--&offset=0")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_sql_injection_in_offset(client_app):
    """test_get_users_sql_injection_in_offset

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=10&offset=0;DROP TABLE users;--")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_invalid_characters_in_limit(client_app):
    """test_get_users_invalid_characters_in_limit

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=abc&offset=0")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_invalid_characters_in_offset(client_app):
    """test_get_users_invalid_characters_in_offset

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=10&offset=abc")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_negative_values(client_app):
    """test_get_users_negative_values

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=-1&offset=-10")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_large_more_limit_error(client_app):
    """test_get_users_large_more_limit_error

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=10000&offset=0")
    assert response.status_code == 422
    

@pytest.mark.asyncio
async def test_get_users_large_limit(client_app):
    """test_get_users_large_limit

    Args:
        client_app (Fastapi): App fixture to requests tests.
    """
    response = client_app.get("/users/?limit=20&offset=0")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    


@pytest.mark.asyncio
async def test_create_user(client_app):
    new_user = SchemaUsers(email="joao.silva@tests.com", name="Joao Silva", nickname="SilvaJ", password="Teste@123")

    response = client_app.post(url="/users/", json=new_user.model_dump())
    
    assert response.status_code == 201
    assert response.json()['email'] == new_user.email
    

@pytest.mark.asyncio
async def test_create_user_email_duplicated(client_app, add_user_to_db):
    
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": "Teste@123.tests"
    }
    
    await add_user_to_db(**new_user_data)
    
    response = client_app.post(url="/users/", json=new_user_data)
    
    assert response.status_code == 400
    assert new_user_data['email'] in response.json()
    assert response.json()['email'] == new_user_data['email']
    assert response.json()['detail'] == "Email already exists"
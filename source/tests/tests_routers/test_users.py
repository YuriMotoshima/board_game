import pytest


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
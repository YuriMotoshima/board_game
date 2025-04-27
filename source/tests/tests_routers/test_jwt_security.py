from http import HTTPStatus

import pytest

from app.security.security import get_password_hash


@pytest.mark.asyncio
async def test_create_token(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)
    
    auth_data = {"username":new_user_data["nickname"], "password":_password}

    response = await client_app_async.post('/token/get_token', data=auth_data)
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()['access_token']
    assert response.json()['token_type'] == 'Bearer'


@pytest.mark.asyncio
async def test_create_token_wrong_password(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)
    
    auth_data = {"username":new_user_data["nickname"], "password":f"{_password}--0"}

    response = await client_app_async.post('/token/get_token', data=auth_data)
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Credenciais inválidas." in response.text
    

@pytest.mark.asyncio
async def test_create_refresh_token(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    # Geração do refresh token fictício
    refresh_token = generate_valid_refresh_token(new_user_data["email"])

    payload = {"refresh_token": refresh_token}

    # Mockar os dados do cache (simulando o sucesso)
    mock_cache_data = {
        "user_agent": "Mozilla/5.0",
        "client_host": "127.0.0.1",
        "geolocation": {"country": "BR"},
        "path": "/token/get_token"
    }

    # Simular a chamada à API
    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    
    
@pytest.mark.asyncio
async def test_create_refresh_token_cache_not_found(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_invalid_refresh_token()  # Gerar um token inválido para o caso de erro

    payload = {"refresh_token": refresh_token}

    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "Cache não encontrado" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_user_agent(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_valid_refresh_token(new_user_data["email"])

    payload = {"refresh_token": refresh_token}

    # Mockar o User-Agent inválido
    mock_cache_data = {
        "user_agent": "InvalidUserAgent",  # User-Agent incorreto
        "client_host": "127.0.0.1",
        "geolocation": {"country": "BR"},
        "path": "/token/get_token"
    }

    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Access refused" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_ip(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_valid_refresh_token(new_user_data["email"])

    payload = {"refresh_token": refresh_token}

    # Mockar o IP inválido
    mock_cache_data = {
        "user_agent": "Mozilla/5.0",
        "client_host": "192.168.0.2",  # IP inválido
        "geolocation": {"country": "BR"},
        "path": "/token/get_token"
    }

    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Access refused" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_country(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_valid_refresh_token(new_user_data["email"])

    payload = {"refresh_token": refresh_token}

    # Mockar o país inválido
    mock_cache_data = {
        "user_agent": "Mozilla/5.0",
        "client_host": "127.0.0.1",
        "geolocation": {"country": "US"},  # País inválido
        "path": "/token/get_token"
    }

    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Access refused" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_email(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_valid_refresh_token("invalid.email@tests.com")  # Email inválido

    payload = {"refresh_token": refresh_token}

    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Access refused" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_refresh_token_expired(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_expired_refresh_token(new_user_data["email"])

    payload = {"refresh_token": refresh_token}

    response = await client_app_async.post('/token/get_refresh', json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Signature has expired" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_refresh_token_internal_error(client_app_async, add_user_to_db, session):
    _password = "Teste@123.tests"
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": get_password_hash(password=_password)
    }
    await add_user_to_db(**new_user_data)

    refresh_token = generate_valid_refresh_token(new_user_data["email"])

    payload = {"refresh_token": refresh_token}

    # Simula uma falha no código
    with pytest.raises(Exception):
        await client_app_async.post('/token/get_refresh', json=payload)

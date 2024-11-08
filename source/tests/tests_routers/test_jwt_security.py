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
from http import HTTPStatus
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.routers.users import (get_user, get_users, 
                               create_user, update_user, 
                               partial_update_user, update_user_password)

from app.schemas.schemas_users import (SchemaPatchUser, SchemaPutUser,
                                       SchemaPutUserPassword,
                                       SchemaResponseUsers, SchemaUsers)

    
@pytest.mark.asyncio
async def test_get_user_directly(add_user_to_db, session):
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": "Teste@123.tests"
    }
    mock_users = await add_user_to_db(**new_user_data)

    response = await get_user(user_id=mock_users.id, session=session)
    
    assert response.id == mock_users.id
    assert response.name == mock_users.name


@pytest.mark.asyncio
async def test_get_user_directly_not_found(session):

    with pytest.raises(HTTPException) as exc_info:
        await get_user(user_id='10001', session=session)
    
    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert "User not found." in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_users_success(add_user_to_db, session):
    
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": "Teste@123.tests"
    }
    await add_user_to_db(**new_user_data)

    response = await get_users(session=session, limit=10, offset=0)
    
    assert isinstance(response.fetchall(), list)


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = SchemaUsers(email="joao.silva@tests.com", name="Joao Silva", nickname="SilvaJ", password="Teste@123")

    response = await create_user(user=new_user, session=session)
    
    assert response.id == 1
    assert response.email == new_user.email
    

@pytest.mark.asyncio
async def test_create_user_email_duplicated(session, add_user_to_db):
    
    new_user_data = SchemaUsers(
        email="tests.joao.silva@tests.com", 
        name="Tests Joao Silva", 
        nickname="TestsSilvaJ", 
        password="Teste@123.tests")
    
    await add_user_to_db(**new_user_data.model_dump())
    
    with pytest.raises(HTTPException) as exc_info:
        await create_user(user=new_user_data, session=session)
    
    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert "Email is already in use." in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_user_nickname_duplicated(session, add_user_to_db):

    new_user_data_duplicated_nickname = SchemaUsers(
        email= "tests0.joao.silva@tests.com",
        name= "Tests0 Joao Silva",
        nickname= "TestsSilvaJ",
        password= "Teste@123.tests"
    )
    
    new_user_data = SchemaUsers(
        email="tests.joao.silva@tests.com", 
        name="Tests Joao Silva", 
        nickname="TestsSilvaJ", 
        password="Teste@123.tests")
    
    await add_user_to_db(**new_user_data.model_dump())
    
    with pytest.raises(HTTPException) as exc_info:
        await create_user(user=new_user_data_duplicated_nickname, session=session)
    
    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert "Nickname is already in use." in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_user_raise_server_error(session):
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": "Teste@123.tests"
    }
    
    with pytest.raises(HTTPException) as exc_info:
        await create_user(user=new_user_data, session=session)
    
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "An unexpected error occurred, verify logs the application." in exc_info.value.detail
    

@pytest.mark.asyncio
async def test_put_update_user_by_email(add_user_to_db, session):
    _user = SchemaPutUser(
        name='Tests Joao Silva',
        email='tests.joao.silva_0@tests.com',
        nickname='TestsSilvaJ'
    )
    
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": "Teste@123.tests"
    }
    await add_user_to_db(**new_user_data)

    response = await update_user(user_id=1, user=_user, session=session)
    
    assert response.email == _user.email


@pytest.mark.asyncio
async def test_put_update_user_not_found(add_user_to_db, session):
    _user = SchemaPutUser(
        name='Tests Joao Silva',
        email='tests.joao.silva_0@tests.com',
        nickname='TestsSilvaJ'
    )
    
    new_user_data = {
        "email": "tests.joao.silva@tests.com",
        "name": "Tests Joao Silva",
        "nickname": "TestsSilvaJ",
        "password": "Teste@123.tests"
    }
    await add_user_to_db(**new_user_data)
    
    with pytest.raises(HTTPException) as exc_info:
        await update_user(user_id=10000, user=_user, session=session)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert "User not found." in exc_info.value.detail
    
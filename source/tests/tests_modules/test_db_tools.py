# tests/tests_database/test_send_to_data.py
import pytest
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.data.models import Users
from app.modules.db_tools import _send_to_data  # Atualize o caminho conforme necessário

@pytest.mark.asyncio
async def test_send_to_data_success(session):
    # Criação de uma instância válida
    new_user = Users(email="joao.silva@tests.com", name="Joao Silva", nickname="SilvaJ", password="Teste@123")
    
    # Chamada da função a ser testada
    result = await _send_to_data(new_user, session)
    
    # Asserções
    assert result == new_user
    assert result.id is not None  # Verifica se o ID foi gerado
    
    # Verifica no banco de dados se o usuário foi realmente adicionado
    fetched_user = await session.get(Users, result.id)
    assert fetched_user is not None
    assert fetched_user.email == "joao.silva@tests.com"


@pytest.mark.asyncio
async def test_send_to_data_integrity_error(session):
    # Criação de duas instâncias com o mesmo email para violar a restrição única
    user1 = Users(email="duplicado@tests.com", name="User One", nickname="User1", password="Password1")
    user2 = Users(email="duplicado@tests.com", name="User Two", nickname="User2", password="Password2")
    
    # Adiciona o primeiro usuário
    await _send_to_data(user1, session)
    
    # Tenta adicionar o segundo usuário, esperando um IntegrityError
    with pytest.raises(HTTPException) as exc_info:
        await _send_to_data(user2, session)
    
    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert "Integrity error" in exc_info.value.detail


@pytest.mark.asyncio
async def test_send_to_data_sqlalchemy_error(session, monkeypatch):
    # Criação de uma instância válida
    new_user = Users(email="erro@tests.com", name="Erro User", nickname="ErroU", password="Erro@123")
    
    # Função simulada que levanta SQLAlchemyError
    async def mock_commit():
        raise SQLAlchemyError("Simulated SQLAlchemy Error")
    
    # Substituindo o método commit da sessão por mock_commit
    monkeypatch.setattr(session, "commit", mock_commit)
    
    # Tenta adicionar o usuário, esperando um SQLAlchemyError
    with pytest.raises(HTTPException) as exc_info:
        await _send_to_data(new_user, session)
    
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Database error" in exc_info.value.detail


@pytest.mark.asyncio
async def test_send_to_data_none_class(session):
    # Chamada da função com db_class como None
    with pytest.raises(HTTPException) as exc_info:
        await _send_to_data(None, session)
    
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "An error occurred while creating the record" in exc_info.value.detail

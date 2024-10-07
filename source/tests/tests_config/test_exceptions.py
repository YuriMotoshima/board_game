import logging

import pytest

from app.config.collections_exceptions import collections_exceptions


# Testes de unidade
def test_collections_exceptions_init():
    exc = collections_exceptions("error message")
    assert exc.args == ("error message",)
    # Adicione mais verificações para os atributos da exceção conforme necessário

# Testes de exceção
def test_collections_exceptions_exception():
    with pytest.raises(Exception):
        # Chame uma função que deve lançar a exceção collections_exceptions
        raise collections_exceptions("error message")

# Testes de log
def test_collections_exceptions_logging(caplog):
    with caplog.at_level(logging.ERROR):
        collections_exceptions("error message")
    assert "error message" in caplog.text
    # Adicione mais verificações conforme necessário

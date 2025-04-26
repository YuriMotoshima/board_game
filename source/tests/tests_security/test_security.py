import pytest
from jwt import decode

from app.security.security import (create_access_token, decode_refresh_token,
                                   get_password_hash, verify_password)


def test_get_password_hash_generates_different_hashes():
    password = "meu_segredo123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    assert hash1 != password
    assert hash2 != password
    assert hash1 != hash2  # hashes com salt devem ser diferentes

def test_verify_password_returns_true_for_correct_password():
    password = "segredo123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True

def test_verify_password_returns_false_for_wrong_password():
    password = "senha123"
    wrong_password = "senha_errada"
    hashed = get_password_hash(password)

    assert verify_password(wrong_password, hashed) is False

def test_create_access_token_contains_exp_and_sub(settings):
    data = {"sub": "test_user@example.com"}
    tokens = create_access_token(data=data)

    decoded_access = decode(tokens["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    decoded_refresh = decode(tokens["refresh_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded_access["sub"] == data["sub"]
    assert "exp" in decoded_access

    assert decoded_refresh["sub"] == data["sub"]
    assert "exp" in decoded_refresh

def test_decode_refresh_token_returns_expected_payload(settings):
    data = {"sub": "refresh_user@example.com"}
    tokens = create_access_token(data=data)

    decoded = decode_refresh_token(tokens["refresh_token"])

    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded

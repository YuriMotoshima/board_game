from datetime import UTC, datetime, timedelta
from secrets import token_hex

from jwt import decode, encode
from pwdlib import PasswordHash

from app import _settings as Settings

pwd_context = PasswordHash.recommended()


def get_password_hash(password:str):
    return pwd_context.hash(password=password)


def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data:dict):
    access_token_expires = datetime.now(UTC) + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.now(UTC) + timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_payload = data.copy()
    access_payload.update({"exp": access_token_expires})

    refresh_payload = data.copy()
    refresh_payload.update({"exp": refresh_token_expires})

    access_token = encode(access_payload, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    refresh_token = encode(refresh_payload, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
def decode_refresh_token(refresh_token:str):
    return decode(refresh_token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])

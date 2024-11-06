from pwdlib import PasswordHash
from jwt import encode, decode
from secrets import token_hex
from app.config.settings import Settings
from datetime import UTC, datetime, timedelta

pwd_context = PasswordHash.recommended()

settings = Settings()

def get_password_hash(password:str):
    return pwd_context.hash(password=password)


def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt
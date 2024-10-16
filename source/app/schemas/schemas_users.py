from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.security.security import get_password_hash


class SchemaMessage(BaseModel):
    message: Optional[str]
    headers: Optional[dict]
    scope: Optional[dict | str]
    state: Optional[dict]


class SchemaUsers(BaseModel):
    name: str
    email: EmailStr
    nickname: str
    password: str
    
    @field_validator('password', mode='before')
    def hash_password(cls, value: str) -> str:
        return get_password_hash(value)


class SchemaResponseUsers(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: EmailStr
    nickname: Optional[str]
    

class SchemaPutUser(BaseModel):
    name: str
    email: EmailStr
    nickname: str


class SchemaPatchUser(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    nickname: Optional[str] = Field(default=None)
    
    
class SchemaPutUserPassword(BaseModel):
    email: EmailStr
    password: str
    new_password: str
    
    @field_validator('new_password', mode='before')
    def hash_password(cls, value: str) -> str:
        return get_password_hash(value)

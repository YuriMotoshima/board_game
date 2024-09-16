from typing import Optional
from pydantic import BaseModel, EmailStr

class SchemaMessage(BaseModel):
    message: Optional[str]
    headers: Optional[dict]
    scope: Optional[dict | str]
    state: Optional[dict]
    
class SchemaUsers(BaseModel):
    name: Optional[str]
    email: EmailStr
    nickname: Optional[str]
    password: str

class SchemaResponseUsers(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: EmailStr
    nickname: Optional[str]
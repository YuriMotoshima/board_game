from typing import Optional
from pydantic import BaseModel

class SchemaMessage(BaseModel):
    message: Optional[str]
    headers: Optional[dict]
    scope: Optional[dict | str]
    state: Optional[dict]
    
class SchemaUsers(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    nickname: Optional[str]
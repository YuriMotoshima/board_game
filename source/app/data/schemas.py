from typing import Optional
from pydantic import BaseModel

class Message(BaseModel):
    message: Optional[str]
    headers: Optional[dict]
    scope: Optional[dict | str]
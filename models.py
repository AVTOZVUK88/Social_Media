from typing import Optional
from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    id_user: int
    username: str
    password: str
    created_at: date
    updated_at: Optional[date]

class Post(BaseModel):
    id_post: int
    user_id: int
    text: str
    created_at: date
    updated_at: Optional[date]
# backend/application/dtos/user_dto.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
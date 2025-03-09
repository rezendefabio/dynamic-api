# backend/application/dtos/auth_dto.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
# backend/interfaces/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.middleware.auth_middleware import get_current_user, get_current_admin
from application.dtos.auth_dto import LoginRequest
from domain.services.auth_service import AuthService
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.database.database import get_db

router = APIRouter()

@router.post("/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    user = user_repo.get_user_by_username(login_data.username)
    if not user or not auth_service.verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth_service.create_access_token(user.username, user.role)
    return {"access_token": token, "token_type": "bearer"}
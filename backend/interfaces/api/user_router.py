from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.middleware.auth_middleware import get_current_user, get_current_admin
from application.dtos.user_dto import UserCreate
from domain.entities.user import User
from domain.services.auth_service import AuthService
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.database.database import get_db

router = APIRouter()

@router.post("/users")
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)  # Garantir que apenas ADMIN pode criar usuários
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    if user_repo.get_user_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    password_hash = auth_service.get_password_hash(user_data.password)
    user_repo.create_user(user_data.username, password_hash, user_data.role)
    return {"message": "User created successfully"}

@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.put("/users/{user_id}")
async def update_user(
        user_id: int,
        user_data: UserCreate,
        db: Session = Depends(get_db),
        current_admin: dict = Depends(get_current_admin)  # Garantir que apenas ADMIN pode alterar usuários
):
    user_repo = UserRepository(db)
    user = user_repo.db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Atualizar os campos do usuário
    user.username = user_data.username
    user.password_hash = AuthService(user_repo).get_password_hash(user_data.password)
    user.role = user_data.role

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_admin: dict = Depends(get_current_admin)  # Garantir que apenas ADMIN pode excluir usuários
):
    user_repo = UserRepository(db)
    user = user_repo.db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Excluir o usuário
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
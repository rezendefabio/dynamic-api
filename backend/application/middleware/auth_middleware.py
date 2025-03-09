# backend/application/middleware/auth_middleware.py
from fastapi import HTTPException, Security, Depends  # Adicionar Depends aqui
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from domain.services.auth_service import AuthService
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.database.database import SessionLocal

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    auth_service = AuthService(UserRepository(SessionLocal()))
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

def get_current_admin(current_user: dict = Depends(get_current_user)):  # Usar Depends aqui
    if current_user.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Permission denied: Admin role required")
    return current_user
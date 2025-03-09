# backend/infrastructure/repositories/user_repository.py
from sqlalchemy.orm import Session
from domain.entities.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, password_hash: str, role: str):
        db_user = User(username=username, password_hash=password_hash, role=role)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
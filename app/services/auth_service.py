from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        
        user_kwargs = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "full_name": user_data.full_name,
        }
        if hasattr(user_data, "role"):
            user_kwargs["role"] = user_data.role

        user = User(**user_kwargs)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def authenticate_user(self, email_or_username: str, password: str) -> Optional[User]:
        # Try email first
        user = self.get_user_by_email(email_or_username)
        if not user:
            # Try username
            user = self.get_user_by_username(email_or_username)
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_access_token(self, user_id: int) -> str:
        return create_access_token(user_id)
    
    def create_refresh_token(self, user_id: int) -> str:
        return create_refresh_token(user_id)
    
    def verify_refresh_token(self, token: str) -> Optional[int]:
        payload = decode_token(token)
        if payload and payload.get("type") == "refresh":
            return int(payload.get("sub"))
        return None
    
    def update_last_login(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            self.db.commit()

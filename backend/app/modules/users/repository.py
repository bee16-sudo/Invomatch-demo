# backend/app/modules/users/repository.py

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.users.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

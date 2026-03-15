# backend/app/modules/users/service.py

from uuid import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRegister


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserRegister) -> tuple[User, str]:
        if self.repo.find_by_email(data.email):
            raise BusinessRuleError("An account with this email already exists")

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
        )
        created = self.repo.create(user)
        token = create_access_token(created.id)
        return created, token

    def login(self, email: str, password: str) -> tuple[User, str]:
        user = self.repo.find_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise BusinessRuleError("Invalid email or password")
        if not user.is_active:
            raise BusinessRuleError("Account is disabled")
        token = create_access_token(user.id)
        return user, token

    def get_by_id(self, user_id: UUID) -> User:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        return user

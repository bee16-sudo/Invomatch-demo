# backend/app/modules/users/routes.py

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessRuleError, NotFoundError
from app.core.security import JWTBearer
from app.modules.users.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.modules.users.service import UserService

router = APIRouter()
auth = JWTBearer()


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        user, token = service.register(data)
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))
    except BusinessRuleError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        user, token = service.login(data.email, data.password)
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))
    except BusinessRuleError as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.get("/me", response_model=UserResponse)
def get_me(payload: dict = Depends(auth), db: Session = Depends(get_db)):
    try:
        service = UserService(db)
        user = service.get_by_id(UUID(payload["sub"]))
        return UserResponse.model_validate(user)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

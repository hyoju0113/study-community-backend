from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from ..repositories import UserRepository
from ..services import AuthService
from ..auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserRegister, service: AuthService = Depends(get_auth_service)):
    user, token = service.register(data)
    return TokenResponse(
        access_token=token,
        user=UserResponse(id=user.id, username=user.username, email=user.email, role=user.role or "user", createdAt=user.created_at),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, service: AuthService = Depends(get_auth_service)):
    user, token = service.login(data)
    return TokenResponse(
        access_token=token,
        user=UserResponse(id=user.id, username=user.username, email=user.email, role=user.role or "user", createdAt=user.created_at),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role or "user",
        createdAt=current_user.created_at,
    )

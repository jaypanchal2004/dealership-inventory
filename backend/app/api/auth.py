from fastapi import APIRouter, status

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    UserRegisterRequest,
    UserResponse,
)
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(data: UserRegisterRequest):
    user = await register_user(data)
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        role=user.role.value,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    token = await authenticate_user(data)
    return TokenResponse(access_token=token)

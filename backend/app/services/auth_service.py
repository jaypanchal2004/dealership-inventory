from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, UserRegisterRequest


async def register_user(data: UserRegisterRequest) -> User:
    """Create a new user, rejecting duplicate emails."""
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    await user.insert()
    return user


async def authenticate_user(data: LoginRequest) -> str:
    """Verify credentials and return a signed JWT access token."""
    user = await User.find_one(User.email == data.email)
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return token

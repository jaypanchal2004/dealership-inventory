from enum import Enum

from beanie import Document
from pydantic import EmailStr


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(Document):
    username: str
    email: EmailStr
    password_hash: str
    role: UserRole = UserRole.CUSTOMER

    class Settings:
        name = "users"

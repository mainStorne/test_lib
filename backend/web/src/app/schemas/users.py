from datetime import datetime
from typing import Optional, TypeVar
from pydantic import EmailStr, BaseModel
from fastapi_users import schemas
from fastapi_sqlalchemy_toolkit import make_partial_model


class UserRead(schemas.BaseUser[int]):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: Optional[EmailStr] = None


UserUpdate = make_partial_model(UserCreate)

UC = TypeVar('UC', bound=UserCreate)

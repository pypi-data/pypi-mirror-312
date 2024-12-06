from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from argon2 import PasswordHasher, exceptions as Ex
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


Ph=PasswordHasher()
class User():
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    password = Column(String(1024),nullable=False)
    lastname = Column(String(256), nullable=False)
    firstname = Column(String(256), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str):
        self.password = Ph.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            Ph.verify(self.password, password)
            return True
        except Ex.VerifyMismatchError:
            return False
        except Ex.InvalidHashError:
            self.set_password(password)
            return self.check_password(password)


class UserBaseModel(BaseModel):
    email: str = Field(example="user@example.com")
    username: str = Field(example="Harlequelrah")
    lastname: str = Field(example="SMITH")
    firstname: str = Field(example="jean-francois")


class UserCreateModel(UserBaseModel):
    password: str = Field(example="m*td*pa**e")


class UserUpdateModel(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserPydanticModel(UserBaseModel):
    id: int
    is_active: bool
    date_created: datetime


class UserLoginModel(BaseModel):
    username: Optional[str] = None
    password: str
    email: Optional[str] = None

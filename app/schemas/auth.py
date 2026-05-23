from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema


class UserRegister(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseSchema):
    email: EmailStr
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"

from datetime import datetime

from pydantic import EmailStr

from app.schemas.base import BaseSchema


class UserRead(BaseSchema):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

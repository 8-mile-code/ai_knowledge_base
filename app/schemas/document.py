from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import BaseSchema


class DocumentBase(BaseModel):
    title: str
    content: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    title: str | None = None
    content: str | None = None


class DocumentRead(BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

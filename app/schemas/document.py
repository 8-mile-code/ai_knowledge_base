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


class DocumentRead(BaseSchema, DocumentBase):
    id: int
    status: str
    processing_error: str | None = None
    processed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

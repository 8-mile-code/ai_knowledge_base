from app.schemas.base import BaseSchema


class AskRequest(BaseSchema):
    question: str


class AskSource(BaseSchema):
    chunk_id: int
    document_id: int
    content: str


class AskResponse(BaseSchema):
    answer: str
    sources: list[AskSource]

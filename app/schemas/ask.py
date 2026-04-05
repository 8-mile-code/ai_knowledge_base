from app.schemas.base import BaseSchema


class AskRequest(BaseSchema):
    question: str
    document_id: int


class AskResponse(BaseSchema):
    answer: str
    sources: list[int]
    chunks: list[str] | None = None

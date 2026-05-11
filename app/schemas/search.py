from app.schemas.base import BaseSchema


class SearchResult(BaseSchema):
    id: int
    document_id: int
    index: int
    content: str

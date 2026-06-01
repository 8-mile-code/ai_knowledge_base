from collections.abc import Callable

import pytest

from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister
from app.schemas.document import DocumentCreate
from app.services.chunk_service import ChunkService


class EmptyChunkRepository:
    pass


@pytest.fixture
def make_user() -> Callable[..., User]:
    def _make_user(
        *,
        id: int = 1,
        email: str = "test@example.com",
        password: str = "hashed-password",
    ) -> User:
        return User(
            id=id,
            email=email,
            password=password,
        )

    return _make_user


@pytest.fixture
def make_document() -> Callable[..., Document]:
    def _make_document(
        *,
        id: int = 1,
        title: str = "Test document",
        content: str = "Some content",
        user_id: int = 1,
        status: str = DocumentStatus.PENDING.value,
    ) -> Document:
        return Document(
            id=id,
            title=title,
            content=content,
            user_id=user_id,
            status=status,
        )

    return _make_document


@pytest.fixture
def make_chunk() -> Callable[..., Chunk]:
    def _make_chunk(
        *,
        id: int = 1,
        content: str = "Chunk content",
        document_id: int = 1,
        index: int = 0,
    ) -> Chunk:
        return Chunk(
            id=id,
            content=content,
            document_id=document_id,
            index=index,
        )

    return _make_chunk


@pytest.fixture
def sample_chunks(make_chunk: Callable[..., Chunk]) -> list[Chunk]:
    return [
        make_chunk(id=1, content="First chunk", index=0),
        make_chunk(id=2, content="Second chunk", index=1),
    ]


@pytest.fixture
def user_register_data() -> UserRegister:
    return UserRegister(
        email="test@example.com",
        password="123456",
    )


@pytest.fixture
def user_login_data() -> UserLogin:
    return UserLogin(
        email="test@example.com",
        password="123456",
    )


@pytest.fixture
def invalid_user_login_data() -> UserLogin:
    return UserLogin(
        email="test@example.com",
        password="wrong-password",
    )


@pytest.fixture
def document_create_data() -> DocumentCreate:
    return DocumentCreate(
        title="Test document",
        content="Some content",
    )


@pytest.fixture
def chunk_service() -> ChunkService:
    return ChunkService(repo=EmptyChunkRepository())

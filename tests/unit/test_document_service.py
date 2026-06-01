from collections.abc import Callable
from unittest.mock import patch

import pytest

from app.core.exceptions import DocumentNotFoundError
from app.models.document import Document
from app.schemas.document import DocumentCreate
from app.services.document_service import DocumentService


class FakeDocumentRepository:
    def __init__(self, make_document: Callable[..., Document]) -> None:
        self.make_document = make_document
        self.documents = []
        self.deleted = True

    async def create(self, db, document_in, user_id):
        document = self.make_document(
            id=1,
            title=document_in.title,
            content=document_in.content,
            user_id=user_id,
        )
        self.documents.append(document)
        return document

    async def get(self, db, document_id, user_id):
        return next(
            (
                document
                for document in self.documents
                if document.id == document_id and document.user_id == user_id
            ),
            None,
        )

    async def get_all(self, db, user_id):
        return [
            document
            for document in self.documents
            if document.user_id == user_id
        ]

    async def delete(self, db, document_id, user_id):
        return self.deleted


class FakeChunkService:
    pass


@pytest.mark.asyncio
async def test_create_document_creates_document_and_starts_task(
    make_document: Callable[..., Document],
    document_create_data: DocumentCreate,
) -> None:
    repo = FakeDocumentRepository(make_document)
    service = DocumentService(repo=repo, chunk_service=FakeChunkService())

    with patch(
        "app.services.document_service.process_document.delay"
    ) as delay:
        document = await service.create_document(
            db=None,
            document_in=document_create_data,
            user_id=10,
        )

    assert document.title == document_create_data.title
    assert document.content == document_create_data.content
    assert document.user_id == 10
    delay.assert_called_once_with(document.id)


@pytest.mark.asyncio
async def test_get_document_raises_error_for_wrong_owner(
    make_document: Callable[..., Document],
) -> None:
    repo = FakeDocumentRepository(make_document)
    service = DocumentService(repo=repo, chunk_service=FakeChunkService())

    repo.documents.append(
        make_document(
            id=1,
            title="Private document",
            content="Secret",
            user_id=1,
        )
    )

    with pytest.raises(DocumentNotFoundError):
        await service.get_document(
            db=None,
            document_id=1,
            user_id=2,
        )


@pytest.mark.asyncio
async def test_delete_document_raises_error_when_document_not_found(
    make_document: Callable[..., Document],
) -> None:
    repo = FakeDocumentRepository(make_document)
    repo.deleted = False
    service = DocumentService(repo=repo, chunk_service=FakeChunkService())

    with pytest.raises(DocumentNotFoundError):
        await service.delete_document(
            db=None,
            document_id=999,
            user_id=1,
        )

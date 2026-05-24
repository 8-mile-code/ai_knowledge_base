from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate
from app.services.chunk_service import ChunkService
from app.tasks.document_tasks import process_document


class DocumentService:
    def __init__(
            self,
            repo: DocumentRepository,
            chunk_service: ChunkService
    ):
        self.repo = repo
        self.chunk_service = chunk_service

    async def create_document(
            self,
            db: AsyncSession,
            document_in: DocumentCreate,
            user_id: int
    ) -> Document:
        document = await self.repo.create(db, document_in, user_id)

        process_document.delay(document.id)
        return document

    async def get_document(
            self,
            db: AsyncSession,
            document_id: int,
            user_id: int,
    ) -> Document | None:
        return await self.repo.get(db, document_id, user_id)

    async def get_documents(
            self,
            db: AsyncSession,
            user_id: int,
    ) -> list[Document]:
        return await self.repo.get_all(db, user_id)

    async def delete_document(
            self,
            db: AsyncSession,
            document_id: int,
            user_id: int,
    ) -> bool:
        return await self.repo.delete(db, document_id, user_id)

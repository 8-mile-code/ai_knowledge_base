from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate
from app.services.chunk_service import ChunkService


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

        await self.chunk_service.create_chunks(
            db,
            document.id,
            document.content
        )
        return document

    async def get_document(
            self,
            db: AsyncSession,
            document_id: int
    ) -> Document | None:
        return await self.repo.get(db, document_id)

    async def get_documents(self, db: AsyncSession) -> list[Document]:
        return await self.repo.get_all(db)

    async def delete_document(
            self,
            db: AsyncSession,
            document_id: int
    ) -> None:
        await self.repo.delete(db, document_id)

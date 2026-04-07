from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate
from app.models.document import Document


class DocumentService:
    def __init__(self, repo: DocumentRepository):
        self.repo = repo

    async def create_document(
            self,
            db: AsyncSession,
            document_in: DocumentCreate,
            user_id: int
    ) -> Document:
        return await self.repo.create(db, document_in, user_id)

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

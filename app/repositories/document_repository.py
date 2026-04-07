from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.schemas.document import DocumentCreate


class DocumentRepository:
    async def create(
            self,
            db: AsyncSession,
            document_in: DocumentCreate,
            user_id: int
    ) -> Document:
        document = Document(
            title=document_in.title,
            content=document_in.content,
            user_id=user_id
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)
        return document

    async def get(self, db: AsyncSession, document_id: int) -> Document | None:
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Document]:
        result = await db.execute(select(Document))
        return result.scalars().all()

    async def delete(self, db: AsyncSession, document_id: int) -> None:
        await db.execute(delete(Document).where(Document.id == document_id))
        await db.commit()

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.repositories.chunk_repository import ChunkRepository


class ChunkService:
    def __init__(self, repo: ChunkRepository):
        self.repo = repo

    def split_text(
            self,
            text: str,
            chunk_size: int = 500,
            overlap: int = 50
    ) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    async def create_chunks(
            self,
            db: AsyncSession,
            document_id: int,
            text: str,
    ):
        texts = self.split_text(text)

        chunks = [
            Chunk(
                document_id=document_id,
                content=chunk_text,
                index=i,
            )
            for i, chunk_text in enumerate(texts)
        ]

        return await self.repo.create_many(db, chunks)

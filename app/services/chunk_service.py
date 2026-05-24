from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.repositories.chunk_repository import ChunkRepository


class ChunkService:
    def __init__(self, repo: ChunkRepository) -> None:
        self.repo = repo

    def split_text(
            self,
            text: str,
            chunk_size: int = 500,
            overlap: int = 50
    ) -> list[str]:
        """Split text into overlapping
        chunks without cutting words when possible.
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            raw_chunk = text[start:end]

            last_space = raw_chunk.rfind(" ")
            if last_space != -1:
                chunk = raw_chunk[:last_space]
            else:
                chunk = raw_chunk

            if chunk.strip():
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    async def create_chunks(
            self,
            db: AsyncSession,
            document_id: int,
            text: str,
    ) -> list[Chunk]:
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

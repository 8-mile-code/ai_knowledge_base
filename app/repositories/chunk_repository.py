from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk


class ChunkRepository:
    async def create_many(
            self,
            db: AsyncSession,
            chunks: list[Chunk],
    ) -> list[Chunk]:
        db.add_all(chunks)
        await db.commit()
        return chunks

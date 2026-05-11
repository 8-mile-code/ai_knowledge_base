from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chunk import Chunk
from app.models.embedding import Embedding


class ChunkRepository:
    async def create_many(
            self,
            db: AsyncSession,
            chunks: list[Chunk],
    ) -> list[Chunk]:
        db.add_all(chunks)
        await db.commit()

        for chunk in chunks:
            await db.refresh(chunk)

        return chunks

    async def get_similar_chunks(
            self,
            db: AsyncSession,
            query_embedding: list[float],
            limit: int = 5
    ) -> list[Chunk]:
        stmt = (
            select(Chunk)
            .join(Embedding)
            .options(selectinload(Chunk.embedding))
            .order_by(Embedding.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chunk import Chunk
from app.models.document import Document
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
            user_id: int,
            limit: int = 5
    ) -> list[Chunk]:
        """Return chunks most similar to the query embedding for one user.

        Results are ordered by pgvector cosine distance and
        filtered by document ownership so users cannot
        retrieve chunks from other users' documents.
        """
        stmt = (
            select(Chunk)
            .join(Embedding)
            .join(Document)
            .where(Document.user_id == user_id)
            .options(selectinload(Chunk.embedding))
            .order_by(Embedding.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService


class SearchService:
    def __init__(
            self,
            embedding_service: EmbeddingService,
            chunk_repo: ChunkRepository
    ):
        self.embedding_service = embedding_service
        self.chunk_repo = chunk_repo

    async def get_similar_chunks(
            self,
            db: AsyncSession,
            query: str,
            user_id: int,
            limit: int = 5
    ) -> list[Chunk]:
        query_embedding = await self.embedding_service.generate_embedding(
            query
        )

        return await self.chunk_repo.get_similar_chunks(
            db=db,
            query_embedding=query_embedding,
            user_id=user_id,
            limit=limit
        )

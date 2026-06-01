import pytest

from app.models.chunk import Chunk
from app.services.search_service import SearchService


class FakeEmbeddingService:
    async def generate_embedding(self, text: str) -> list[float]:
        self.text = text
        return [0.1, 0.2, 0.3]


class FakeChunkRepository:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks

    async def get_similar_chunks(
        self,
        db,
        query_embedding,
        user_id: int,
        limit: int = 5,
    ):
        self.query_embedding = query_embedding
        self.user_id = user_id
        self.limit = limit

        return self.chunks


@pytest.mark.asyncio
async def test_get_similar_chunks_generates_embedding_and_searches_chunks(
    sample_chunks: list[Chunk],
) -> None:
    embedding_service = FakeEmbeddingService()
    chunk_repo = FakeChunkRepository(sample_chunks)
    service = SearchService(
        embedding_service=embedding_service,
        chunk_repo=chunk_repo,
    )

    chunks = await service.get_similar_chunks(
        db=None,
        query="What is pgvector?",
        user_id=10,
        limit=3,
    )

    assert embedding_service.text == "What is pgvector?"
    assert chunk_repo.query_embedding == [0.1, 0.2, 0.3]
    assert chunk_repo.user_id == 10
    assert chunk_repo.limit == 3
    assert len(chunks) == 2

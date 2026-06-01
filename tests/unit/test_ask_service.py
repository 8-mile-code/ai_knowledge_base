import pytest

from app.models.chunk import Chunk
from app.services.ask_service import AskService


class FakeSearchService:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks

    async def get_similar_chunks(
        self,
        db,
        query: str,
        user_id: int,
        limit: int = 5,
    ):
        self.query = query
        self.user_id = user_id
        self.limit = limit

        return self.chunks


class FakeLLMService:
    async def generate_answer(self, question: str, context: str) -> str:
        self.question = question
        self.context = context
        return "Generated answer"


@pytest.mark.asyncio
async def test_ask_uses_search_chunks_and_generates_answer(
    sample_chunks: list[Chunk],
) -> None:
    search_service = FakeSearchService(sample_chunks)
    llm_service = FakeLLMService()
    service = AskService(
        search_service=search_service,
        llm_service=llm_service,
    )

    answer, chunks = await service.ask(
        db=None,
        question="What is RAG?",
        user_id=10,
        limit=2,
    )

    assert answer == "Generated answer"
    assert len(chunks) == 2
    assert search_service.query == "What is RAG?"
    assert search_service.user_id == 10
    assert search_service.limit == 2
    assert llm_service.question == "What is RAG?"
    assert "First chunk" in llm_service.context
    assert "Second chunk" in llm_service.context


def test_build_context_joins_chunk_content(sample_chunks: list[Chunk]) -> None:
    service = AskService(
        search_service=FakeSearchService(sample_chunks),
        llm_service=FakeLLMService(),
    )

    context = service._build_context(sample_chunks)

    assert context == "Chunk 1: \nFirst chunk\n\nChunk 2: \nSecond chunk"

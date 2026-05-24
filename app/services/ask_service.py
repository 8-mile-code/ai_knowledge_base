from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.services.llm_service import LLMService
from app.services.search_service import SearchService


class AskService:
    def __init__(
            self,
            search_service: SearchService,
            llm_service: LLMService
    ) -> None:
        self.search_service = search_service
        self.llm_service = llm_service

    async def ask(
            self,
            db: AsyncSession,
            question: str,
            user_id: int,
            limit: int = 5,
    ) -> tuple[str, list[Chunk]]:
        chunks = await self.search_service.get_similar_chunks(
            db=db,
            query=question,
            user_id=user_id,
            limit=limit
        )

        context = self._build_context(chunks)

        answer = await self.llm_service.generate_answer(
            question=question,
            context=context,
        )

        return answer, chunks

    def _build_context(self, chunks: list[Chunk]) -> str:
        """Build RAG context from retrieved chunks for the LLM prompt."""
        return "\n\n".join(
            f"Chunk {chunk.id}: \n{chunk.content}"
            for chunk in chunks
        )

from openai import AsyncOpenAI

from app.core.config import settings
from app.services.cache_service import CacheService


class LLMService:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_LLM_MODEL

    async def generate_answer(
            self,
            question: str,
            context: str,
    ) -> str:
        cached_key = CacheService.build_key(
            "llm_answer",
            self.model,
            question,
            context,
        )
        cached_answer = await CacheService.get_json(cached_key)

        if cached_answer is not None:
            return cached_answer

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant for answering questions based "
                        "only on the provided context. If the answer is not "
                        "in the context, say that you do not have enough "
                        "information."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Context:\n{context}\n\n"
                        f"Question:\n{question}"
                    ),
                },
            ],
            temperature=0.2,
        )
        answer = response.choices[0].message.content or ""

        await CacheService.set_json(
            cached_key,
            answer,
            ttl=60 * 60 * 24,
        )

        return answer

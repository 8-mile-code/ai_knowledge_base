from openai import AsyncOpenAI

from app.core.config import settings
from app.services.cache_service import CacheService


class EmbeddingService:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBEDDING_MODEL

    async def generate_embedding(self, text: str) -> list[float]:
        cached_key = CacheService.build_key(
            "embedding",
            self.model,
            text,
        )

        cached_embedding = await CacheService.get_json(cached_key)

        if cached_embedding is not None:
            return cached_embedding

        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        embedding = response.data[0].embedding

        await CacheService.set_json(
            cached_key,
            embedding,
            ttl=60 * 60 * 24,
        )

        return embedding

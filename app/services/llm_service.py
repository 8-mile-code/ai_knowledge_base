from openai import AsyncOpenAI

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_LLM_MODEL

    async def generate_answer(
            self,
            question: str,
            context: str,
    ) -> str:

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

        return response.choices[0].message.content or ""

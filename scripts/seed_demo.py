import asyncio
from datetime import datetime, timezone

from sqlalchemy import delete, select

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.models.embedding import Embedding
from app.models.user import User
from app.services.embedding_service import EmbeddingService


DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo_password"

DEMO_TITLE = "Demo RAG Knowledge Base"
DEMO_CONTENT = """
AI Knowledge Base is a RAG backend service.

It allows users to upload documents, split them into chunks,
generate vector embeddings, store them in PostgreSQL with pgvector,
perform semantic search, and generate answers using an LLM.

RAG means Retrieval-Augmented Generation.
The system first finds relevant chunks from the knowledge base,
then passes them as context to the language model.

This demo document is used to quickly test the /ask endpoint.
"""


def split_text(text: str, chunk_size: int = 500) -> list[str]:
    return [
        text[i: i + chunk_size].strip()
        for i in range(0, len(text), chunk_size)
        if text[i: i + chunk_size].strip()
    ]


async def seed_demo() -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == DEMO_EMAIL)
        )
        demo_user = result.scalar_one_or_none()

        if demo_user:
            await db.execute(
                delete(Document).where(Document.user_id == demo_user.id)
            )
            await db.commit()
        else:
            demo_user = User(
                email=DEMO_EMAIL,
                password=hash_password(DEMO_PASSWORD),
            )
            db.add(demo_user)
            await db.commit()
            await db.refresh(demo_user)

        document = Document(
            title=DEMO_TITLE,
            content=DEMO_CONTENT,
            status=DocumentStatus.COMPLETED.value,
            processed_at=datetime.now(timezone.utc),
            user_id=demo_user.id,
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)

        embedding_service = EmbeddingService()

        for index, chunk_text in enumerate(split_text(DEMO_CONTENT)):
            chunk = Chunk(
                content=chunk_text,
                index=index,
                document_id=document.id,
            )
            db.add(chunk)
            await db.commit()
            await db.refresh(chunk)

            vector = await embedding_service.generate_embedding(chunk_text)

            embedding = Embedding(
                embedding=vector,
                chunk_id=chunk.id,
            )
            db.add(embedding)
            await db.commit()

    print("Demo data created successfully.")
    print(f"Demo user: {DEMO_EMAIL}")
    print(f"Demo password: {DEMO_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed_demo())

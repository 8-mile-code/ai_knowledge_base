import asyncio

from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.embedding import Embedding
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService


@celery_app.task
def process_document(document_id: int):
    asyncio.run(_process_document(document_id))


async def _process_document(document_id: int):
    async with AsyncSessionLocal() as session:

        document_repo = DocumentRepository()
        chunk_repo = ChunkRepository()
        chunk_service = ChunkService(chunk_repo)

        document = await document_repo.get(session, document_id)

        if not document:
            return

        chunks = await chunk_service.create_chunks(
            session,
            document_id=document.id,
            text=document.content
        )
        embedding_service = EmbeddingService()

        for chunk in chunks:
            vector = await embedding_service.generate_embedding(chunk.content)

            embedding = Embedding(
                chunk_id=chunk.id,
                embedding=vector,
            )

            session.add(embedding)
        
        await session.commit()

        print(f"Chunks and embeddings created for document {document_id}")

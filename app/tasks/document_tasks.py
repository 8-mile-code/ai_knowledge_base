import asyncio
from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.services.chunk_service import ChunkService


@celery_app.task
def process_document(document_id: int):
    asyncio.run(_proccess_document(document_id))


async def _proccess_document(document_id: int):
    async with AsyncSessionLocal() as session:

        document_repo = DocumentRepository()
        chunk_repo = ChunkRepository()
        chunk_service = ChunkService(chunk_repo)

        document = await document_repo.get(session, document_id)

        if not document:
            return

        await chunk_service.create_chunks(
            session,
            document_id=document.id,
            text=document.content
        )
        print(f"Chunks created for document {document_id}")

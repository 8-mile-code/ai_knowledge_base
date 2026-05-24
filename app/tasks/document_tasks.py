from datetime import UTC, datetime

from celery.utils.log import get_task_logger
from sqlalchemy import delete, select

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.models.embedding import Embedding
from app.repositories.chunk_repository import ChunkRepository
from app.services.chunk_service import ChunkService
from app.services.sync_embedding_service import SyncEmbeddingService

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_document(self, document_id: int) -> None:
    """Process a document in the Celery worker.

    Splits text into chunks, generates
    embeddings, and updates processing status.
    """
    try:
        _process_document(document_id)
    except Exception as exc:
        _mark_document_failed(document_id, str(exc))
        raise


def _process_document(document_id: int) -> None:
    chunk_service = ChunkService(ChunkRepository())
    embedding_service = SyncEmbeddingService()

    with SessionLocal() as session:
        document = session.get(Document, document_id)
        if not document:
            logger.info("Document %s not found, skipping", document_id)
            return

        document.status = DocumentStatus.PROCESSING.value
        document.processing_error = None
        document.processed_at = None
        content = document.content
        session.commit()

    chunk_texts = chunk_service.split_text(content)
    if not chunk_texts:
        raise ValueError(
            "Document content is empty or cannot be split into chunks"
        )

    vectors = embedding_service.generate_embeddings(chunk_texts)

    with SessionLocal() as session:
        document = session.execute(
            select(Document)
            .where(Document.id == document_id)
            .with_for_update()
        ).scalar_one_or_none()

        if not document:
            logger.info(
                "Document %s was deleted during processing", document_id
            )
            return

        session.execute(delete(Chunk).where(Chunk.document_id == document_id))
        session.flush()

        chunks = [
            Chunk(
                document_id=document_id,
                content=chunk_text,
                index=index,
            )
            for index, chunk_text in enumerate(chunk_texts)
        ]
        session.add_all(chunks)
        session.flush()

        embeddings = [
            Embedding(chunk_id=chunk.id, embedding=vector)
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
        session.add_all(embeddings)

        document.status = DocumentStatus.COMPLETED.value
        document.processing_error = None
        document.processed_at = datetime.now(UTC)

        session.commit()
        logger.info(
            "Chunks and embeddings created for document %s",
            document_id,
        )


def _mark_document_failed(document_id: int, error_message: str) -> None:
    with SessionLocal() as session:
        document = session.get(Document, document_id)
        if not document:
            return

        document.status = DocumentStatus.FAILED.value
        document.processing_error = error_message[:4000]
        session.commit()

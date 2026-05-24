from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentRead
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService

chunk_service = ChunkService(ChunkRepository())

document_service = DocumentService(
    DocumentRepository(),
    chunk_service
)

router = APIRouter(prefix="/documents", tags=["📑 Documents"])


@router.post(
        "/",
        response_model=DocumentRead,
        summary="Create a new document",
    )
async def create_document(
    document_in: DocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = await document_service.create_document(
        db,
        document_in,
        user_id=current_user.id,
    )
    return document


@router.get(
        "",
        response_model=list[DocumentRead],
        summary="Get all documents",
    )
async def get_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await document_service.get_documents(db, user_id=current_user.id)


@router.get(
        "/{document_id}",
        response_model=DocumentRead,
        summary="Get a document by ID",
    )
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = await document_service.get_document(
        db,
        document_id=document_id,
        user_id=current_user.id,
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete(
        "/{document_id}", summary="Delete a document by ID"
    )
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await document_service.delete_document(
            db,
            document_id=document_id,
            user_id=current_user.id,
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"status": "Document deleted"}

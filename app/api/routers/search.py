from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.chunk_repository import ChunkRepository
from app.schemas.search import SearchResult
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService


search_service = SearchService(
        embedding_service=EmbeddingService(),
        chunk_repo=ChunkRepository()
    )

router = APIRouter(prefix="/search", tags=["🔍 Search"])


@router.get(
    "/",
    response_model=list[SearchResult],
    summary="Search for relevant chunks based on a query"
)
async def search(
    query: str,
    db: AsyncSession = Depends(get_db)
):

    chunks = await search_service.get_similar_chunks(
        db=db,
        query=query,
        limit=5
    )

    return chunks

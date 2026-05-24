from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_search_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.search import SearchResult
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["🔍 Search"])


@router.get(
    "/",
    response_model=list[SearchResult],
    summary="Search for relevant chunks based on a query"
)
async def search(
    query: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search_service: SearchService = Depends(get_search_service),
):

    chunks = await search_service.get_similar_chunks(
        db=db,
        query=query,
        user_id=current_user.id,
        limit=5,
    )

    return chunks

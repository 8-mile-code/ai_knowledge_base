from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.chunk_repository import ChunkRepository
from app.schemas.ask import AskRequest, AskResponse, AskSource
from app.services.ask_service import AskService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.search_service import SearchService

search_service = SearchService(
    embedding_service=EmbeddingService(),
    chunk_repo=ChunkRepository()
)

ask_service = AskService(
    search_service=search_service,
    llm_service=LLMService()
)

router = APIRouter(prefix="/ask", tags=["🤖 Ask"])


@router.post(
    "/",
    response_model=AskResponse,
    summary="Ask a question based on the indexed content",
)
async def ask_question(
    request: AskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer, chunks = await ask_service.ask(
        db=db,
        question=request.question,
        user_id=current_user.id,
        limit=5,
    )

    return AskResponse(
        answer=answer,
        sources=[
            AskSource(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
            )
            for chunk in chunks
        ],
    )

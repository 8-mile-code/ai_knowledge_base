from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_ask_service, get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ask import AskRequest, AskResponse, AskSource
from app.services.ask_service import AskService

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
    ask_service: AskService = Depends(get_ask_service),
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

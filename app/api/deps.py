from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.user_repository import UserRepository
from app.services.ask_service import AskService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.search_service import SearchService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
) -> User:
    """Validate JWT access token and return the authenticated user.

    The token subject (`sub`) is treated as the user ID. The user is loaded
    from the database to ensure the account still exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except ValueError as error:
        raise credentials_exception from error

    try:
        user_id = int(user_id)
    except ValueError as error:
        raise credentials_exception from error

    user = await UserRepository().get_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user


def get_search_service() -> SearchService:
    return SearchService(
        embedding_service=EmbeddingService(),
        chunk_repo=ChunkRepository(),
    )


def get_ask_service() -> AskService:
    return AskService(
        search_service=get_search_service(),
        llm_service=LLMService(),
    )

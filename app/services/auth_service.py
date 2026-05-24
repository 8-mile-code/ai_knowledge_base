from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.security import (create_access_token, hash_password,
                               verify_password)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token, UserLogin, UserRegister


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_user(
            self,
            db: AsyncSession,
            user_in: UserRegister
    ) -> User:
        existing_user = await self.repo.get_by_email(db, user_in.email)
        if existing_user:
            raise UserAlreadyExistsError()

        hashed_password = hash_password(user_in.password)
        user = await self.repo.create(
            db=db,
            email=user_in.email,
            hashed_password=hashed_password
        )
        return user

    async def authenticate_user(
            self,
            db: AsyncSession,
            user_in: UserLogin
    ) -> Token:
        user = await self.repo.get_by_email(db, user_in.email)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(user_in.password, user.password):
            raise InvalidCredentialsError()

        access_token = create_access_token(subject=user.id)

        return Token(access_token=access_token)

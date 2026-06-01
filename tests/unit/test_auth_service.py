from collections.abc import Callable

import pytest

from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister
from app.services.auth_service import AuthService


class FakeUserRepository(UserRepository):
    def __init__(self, make_user: Callable[..., User]) -> None:
        self.make_user = make_user
        self.users = []

    async def get_by_email(self, db, email):
        return next((user for user in self.users if user.email == email), None)

    async def create(self, db, email, hashed_password):
        user = self.make_user(
            id=len(self.users) + 1,
            email=email,
            password=hashed_password,
        )
        self.users.append(user)
        return user


@pytest.mark.asyncio
async def test_register_user_hashes_password(
    make_user: Callable[..., User],
    user_register_data: UserRegister,
) -> None:
    repo = FakeUserRepository(make_user)
    service = AuthService(repo=repo)

    user = await service.register_user(
        db=None,
        user_in=user_register_data,
    )

    assert user.email == user_register_data.email
    assert user.password != user_register_data.password
    assert verify_password(user_register_data.password, user.password) is True


@pytest.mark.asyncio
async def test_register_user_raises_error_for_existing_email(
    make_user: Callable[..., User],
    user_register_data: UserRegister,
) -> None:
    repo = FakeUserRepository(make_user)
    service = AuthService(repo=repo)

    await service.register_user(db=None, user_in=user_register_data)

    with pytest.raises(UserAlreadyExistsError):
        await service.register_user(db=None, user_in=user_register_data)


@pytest.mark.asyncio
async def test_authenticate_user_returns_token(
    make_user: Callable[..., User],
    user_register_data: UserRegister,
    user_login_data: UserLogin,
) -> None:
    repo = FakeUserRepository(make_user)
    service = AuthService(repo=repo)

    await service.register_user(
        db=None,
        user_in=user_register_data,
    )

    token = await service.authenticate_user(
        db=None,
        user_in=user_login_data,
    )

    assert token.access_token
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_authenticate_user_raises_error_for_wrong_password(
    make_user: Callable[..., User],
    user_register_data: UserRegister,
    invalid_user_login_data: UserLogin,
) -> None:
    repo = FakeUserRepository(make_user)
    service = AuthService(repo=repo)

    await service.register_user(
        db=None,
        user_in=user_register_data,
    )

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate_user(
            db=None,
            user_in=invalid_user_login_data,
        )

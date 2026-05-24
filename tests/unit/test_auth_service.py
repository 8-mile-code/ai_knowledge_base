from types import SimpleNamespace

import pytest

from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.security import verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister
from app.services.auth_service import AuthService


class FakeUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users = []

    async def get_by_email(self, db, email):
        return next((user for user in self.users if user.email == email), None)

    async def create(self, db, email, hashed_password):
        user = SimpleNamespace(
            id=len(self.users) + 1,
            email=email,
            password=hashed_password,
        )
        self.users.append(user)
        return user


@pytest.mark.asyncio
async def test_register_user_hashes_password() -> None:
    repo = FakeUserRepository()
    service = AuthService(repo=repo)

    user = await service.register_user(
        db=None,
        user_in=UserRegister(
            email="test@example.com",
            password="123456",
        ),
    )

    assert user.email == "test@example.com"
    assert user.password != "123456"
    assert verify_password("123456", user.password) is True


@pytest.mark.asyncio
async def test_register_user_raises_error_for_existing_email() -> None:
    repo = FakeUserRepository()
    service = AuthService(repo=repo)

    user_in = UserRegister(
        email="test@example.com",
        password="123456",
    )

    await service.register_user(db=None, user_in=user_in)

    with pytest.raises(UserAlreadyExistsError):
        await service.register_user(db=None, user_in=user_in)


@pytest.mark.asyncio
async def test_authenticate_user_returns_token() -> None:
    repo = FakeUserRepository()
    service = AuthService(repo=repo)

    await service.register_user(
        db=None,
        user_in=UserRegister(
            email="test@example.com",
            password="123456",
        ),
    )

    token = await service.authenticate_user(
        db=None,
        user_in=UserLogin(
            email="test@example.com",
            password="123456",
        ),
    )

    assert token.access_token
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_authenticate_user_raises_error_for_wrong_password() -> None:
    repo = FakeUserRepository()
    service = AuthService(repo=repo)

    await service.register_user(
        db=None,
        user_in=UserRegister(
            email="test@example.com",
            password="123456",
        ),
    )

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate_user(
            db=None,
            user_in=UserLogin(
                email="test@example.com",
                password="wrong-password",
            ),
        )

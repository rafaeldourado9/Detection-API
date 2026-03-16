from __future__ import annotations

import uuid
from unittest.mock import AsyncMock

import pytest

from src.application.user.commands import LoginCommand, RegisterUserCommand
from src.application.user.handlers import LoginHandler, RegisterUserHandler
from src.domain.user.entities import User
from src.domain.user.exceptions import InvalidCredentialsError, UserAlreadyExistsError


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


class TestRegisterUserHandler:
    async def test_register_new_user(self, user_repo: AsyncMock) -> None:
        user_repo.find_by_email.return_value = None
        handler = RegisterUserHandler(user_repo)
        user = await handler.handle(RegisterUserCommand(email="a@b.com", password="pass123"))
        assert user.email.value == "a@b.com"
        user_repo.save.assert_awaited_once()

    async def test_register_duplicate_raises(self, user_repo: AsyncMock) -> None:
        user_repo.find_by_email.return_value = User.create("a@b.com", "hash")
        handler = RegisterUserHandler(user_repo)
        with pytest.raises(UserAlreadyExistsError):
            await handler.handle(RegisterUserCommand(email="a@b.com", password="pass"))


class TestLoginHandler:
    async def test_login_invalid_email_raises(self, user_repo: AsyncMock) -> None:
        user_repo.find_by_email.return_value = None
        handler = LoginHandler(user_repo)
        with pytest.raises(InvalidCredentialsError):
            await handler.handle(LoginCommand(email="no@exist.com", password="pass"))

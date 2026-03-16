from __future__ import annotations

from src.application.user.commands import LoginCommand, RegisterUserCommand
from src.domain.user.entities import User
from src.domain.user.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from src.domain.user.repository import UserRepository
from src.infrastructure.auth.jwt import create_access_token
from src.infrastructure.auth.password import hash_password, verify_password


class RegisterUserHandler:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def handle(self, command: RegisterUserCommand) -> User:
        existing = await self._repo.find_by_email(command.email)
        if existing:
            raise UserAlreadyExistsError(command.email)

        hashed = hash_password(command.password)
        user = User.create(email=command.email, hashed_password=hashed)
        await self._repo.save(user)
        return user


class LoginHandler:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def handle(self, command: LoginCommand) -> str:
        user = await self._repo.find_by_email(command.email)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(command.password, user.hashed_password.value):
            raise InvalidCredentialsError()

        return create_access_token(str(user.id))

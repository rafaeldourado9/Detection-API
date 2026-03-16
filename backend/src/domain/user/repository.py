from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.domain.user.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def find_by_id(self, user_id: uuid.UUID) -> User | None: ...

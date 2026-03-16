from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from src.domain.user.value_objects import Email, HashedPassword


@dataclass
class User:
    email: Email
    hashed_password: HashedPassword
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True

    @staticmethod
    def create(email: str, hashed_password: str) -> User:
        return User(
            email=Email(email),
            hashed_password=HashedPassword(hashed_password),
        )

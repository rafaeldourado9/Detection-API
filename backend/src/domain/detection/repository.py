from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.domain.detection.entities import Detection


class DetectionRepository(ABC):
    @abstractmethod
    async def save(self, detection: Detection) -> None: ...

    @abstractmethod
    async def find_by_id(self, detection_id: uuid.UUID) -> Detection | None: ...

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID, limit: int = 50, offset: int = 0) -> list[Detection]: ...

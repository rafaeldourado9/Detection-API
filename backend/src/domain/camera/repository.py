from abc import ABC, abstractmethod
import uuid

from src.domain.camera.entities import Camera


class CameraRepository(ABC):
    @abstractmethod
    async def save(self, camera: Camera) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, camera_id: uuid.UUID) -> Camera | None:
        pass

    @abstractmethod
    async def find_by_user(self, user_id: uuid.UUID) -> list[Camera]:
        pass

    @abstractmethod
    async def delete(self, camera_id: uuid.UUID) -> None:
        pass

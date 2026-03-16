import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.camera.entities import Camera
from src.domain.camera.repository import CameraRepository
from src.infrastructure.persistence.models import CameraModel


class SqlAlchemyCameraRepository(CameraRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, camera: Camera) -> None:
        model = CameraModel(
            id=camera.id,
            user_id=camera.user_id,
            name=camera.name,
            url=camera.url,
            camera_type=camera.camera_type,
            status=camera.status,
            created_at=camera.created_at,
            last_detection_at=camera.last_detection_at,
        )
        self._session.add(model)
        await self._session.commit()

    async def find_by_id(self, camera_id: uuid.UUID) -> Camera | None:
        result = await self._session.execute(select(CameraModel).where(CameraModel.id == camera_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Camera(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            url=model.url,
            camera_type=model.camera_type,
            status=model.status,
            created_at=model.created_at,
            last_detection_at=model.last_detection_at,
        )

    async def find_by_user(self, user_id: uuid.UUID) -> list[Camera]:
        result = await self._session.execute(select(CameraModel).where(CameraModel.user_id == user_id))
        models = result.scalars().all()
        return [
            Camera(
                id=m.id,
                user_id=m.user_id,
                name=m.name,
                url=m.url,
                camera_type=m.camera_type,
                status=m.status,
                created_at=m.created_at,
                last_detection_at=m.last_detection_at,
            )
            for m in models
        ]

    async def delete(self, camera_id: uuid.UUID) -> None:
        result = await self._session.execute(select(CameraModel).where(CameraModel.id == camera_id))
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.commit()

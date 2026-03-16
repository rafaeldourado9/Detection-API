import uuid
from datetime import datetime, timezone

from src.application.camera.commands import CreateCameraCommand, StartCameraCommand, StopCameraCommand
from src.domain.camera.entities import Camera
from src.domain.camera.repository import CameraRepository
from src.domain.camera.value_objects import CameraStatus


class CreateCameraHandler:
    def __init__(self, repo: CameraRepository) -> None:
        self._repo = repo

    async def handle(self, cmd: CreateCameraCommand) -> Camera:
        camera = Camera(
            id=uuid.uuid4(),
            user_id=cmd.user_id,
            name=cmd.name,
            url=cmd.url,
            camera_type=cmd.camera_type,
            status=CameraStatus.INACTIVE,
            created_at=datetime.now(timezone.utc),
        )
        await self._repo.save(camera)
        return camera


class StartCameraHandler:
    def __init__(self, repo: CameraRepository) -> None:
        self._repo = repo

    async def handle(self, cmd: StartCameraCommand) -> Camera:
        camera = await self._repo.find_by_id(cmd.camera_id)
        if not camera:
            raise ValueError("Camera not found")
        camera.status = CameraStatus.ACTIVE
        await self._repo.save(camera)
        return camera


class StopCameraHandler:
    def __init__(self, repo: CameraRepository) -> None:
        self._repo = repo

    async def handle(self, cmd: StopCameraCommand) -> Camera:
        camera = await self._repo.find_by_id(cmd.camera_id)
        if not camera:
            raise ValueError("Camera not found")
        camera.status = CameraStatus.INACTIVE
        await self._repo.save(camera)
        return camera

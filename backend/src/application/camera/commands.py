from dataclasses import dataclass
import uuid

from src.domain.camera.value_objects import CameraType


@dataclass(frozen=True)
class CreateCameraCommand:
    user_id: uuid.UUID
    name: str
    url: str
    camera_type: CameraType


@dataclass(frozen=True)
class StartCameraCommand:
    camera_id: uuid.UUID


@dataclass(frozen=True)
class StopCameraCommand:
    camera_id: uuid.UUID

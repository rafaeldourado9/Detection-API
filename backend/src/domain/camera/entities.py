from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from src.domain.camera.value_objects import CameraStatus, CameraType


@dataclass
class Camera:
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    url: str
    camera_type: CameraType
    status: CameraStatus
    created_at: datetime
    last_detection_at: datetime | None = None

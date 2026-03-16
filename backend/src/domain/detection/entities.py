from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.domain.detection.value_objects import (
    DetectedObject,
    DetectionStatus,
    ImageRef,
)


@dataclass
class Detection:
    """Aggregate root for a detection request."""

    image: ImageRef
    user_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: DetectionStatus = DetectionStatus.PENDING
    objects: list[DetectedObject] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None

    def mark_processing(self) -> None:
        self.status = DetectionStatus.PROCESSING

    def complete(self, detected_objects: list[DetectedObject]) -> None:
        self.status = DetectionStatus.DONE
        self.objects = detected_objects
        self.finished_at = datetime.now(UTC)

    def fail(self) -> None:
        self.status = DetectionStatus.FAILED
        self.finished_at = datetime.now(UTC)

    @staticmethod
    def create(image_path: str, user_id: uuid.UUID) -> Detection:
        return Detection(image=ImageRef(image_path), user_id=user_id)

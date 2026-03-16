from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DetectionStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


@dataclass(frozen=True)
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def __post_init__(self) -> None:
        if self.x_min >= self.x_max or self.y_min >= self.y_max:
            raise ValueError("Invalid bounding box coordinates")


@dataclass(frozen=True)
class Confidence:
    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"Confidence must be between 0 and 1, got {self.value}")


@dataclass(frozen=True)
class ImageRef:
    path: str

    def __post_init__(self) -> None:
        if not self.path:
            raise ValueError("Image path cannot be empty")


@dataclass(frozen=True)
class DetectedObject:
    label: str
    confidence: Confidence
    bbox: BoundingBox

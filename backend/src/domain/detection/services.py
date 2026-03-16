from __future__ import annotations

from src.domain.detection.value_objects import DetectedObject


class DetectionService:
    """Pure domain service — business rules without side effects."""

    @staticmethod
    def filter_by_confidence(
        objects: list[DetectedObject], min_confidence: float = 0.5
    ) -> list[DetectedObject]:
        return [o for o in objects if o.confidence.value >= min_confidence]

    @staticmethod
    def filter_by_labels(
        objects: list[DetectedObject], labels: set[str]
    ) -> list[DetectedObject]:
        return [o for o in objects if o.label in labels]

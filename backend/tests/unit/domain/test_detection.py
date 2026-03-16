import uuid

import pytest

from src.domain.detection.entities import Detection
from src.domain.detection.services import DetectionService
from src.domain.detection.value_objects import (
    BoundingBox,
    Confidence,
    DetectedObject,
    DetectionStatus,
    ImageRef,
)


class TestBoundingBox:
    def test_valid_bbox(self) -> None:
        bbox = BoundingBox(x_min=0, y_min=0, x_max=100, y_max=100)
        assert bbox.x_max == 100

    def test_invalid_bbox_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid bounding box"):
            BoundingBox(x_min=100, y_min=0, x_max=50, y_max=100)


class TestConfidence:
    def test_valid_confidence(self) -> None:
        c = Confidence(0.95)
        assert c.value == 0.95

    def test_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError, match="between 0 and 1"):
            Confidence(1.5)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="between 0 and 1"):
            Confidence(-0.1)


class TestImageRef:
    def test_valid_path(self) -> None:
        ref = ImageRef("/uploads/img.jpg")
        assert ref.path == "/uploads/img.jpg"

    def test_empty_path_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            ImageRef("")


class TestDetection:
    def test_create_detection(self) -> None:
        uid = uuid.uuid4()
        d = Detection.create(image_path="/img.jpg", user_id=uid)
        assert d.status == DetectionStatus.PENDING
        assert d.user_id == uid
        assert d.objects == []

    def test_mark_processing(self) -> None:
        d = Detection.create(image_path="/img.jpg", user_id=uuid.uuid4())
        d.mark_processing()
        assert d.status == DetectionStatus.PROCESSING

    def test_complete(self) -> None:
        d = Detection.create(image_path="/img.jpg", user_id=uuid.uuid4())
        objs = [
            DetectedObject(
                label="person",
                confidence=Confidence(0.9),
                bbox=BoundingBox(0, 0, 50, 50),
            )
        ]
        d.complete(objs)
        assert d.status == DetectionStatus.DONE
        assert len(d.objects) == 1
        assert d.finished_at is not None

    def test_fail(self) -> None:
        d = Detection.create(image_path="/img.jpg", user_id=uuid.uuid4())
        d.fail()
        assert d.status == DetectionStatus.FAILED
        assert d.finished_at is not None


class TestDetectionService:
    def _make_objects(self) -> list[DetectedObject]:
        return [
            DetectedObject("person", Confidence(0.9), BoundingBox(0, 0, 10, 10)),
            DetectedObject("car", Confidence(0.3), BoundingBox(10, 10, 20, 20)),
            DetectedObject("dog", Confidence(0.7), BoundingBox(20, 20, 30, 30)),
        ]

    def test_filter_by_confidence(self) -> None:
        objs = self._make_objects()
        filtered = DetectionService.filter_by_confidence(objs, min_confidence=0.5)
        assert len(filtered) == 2
        labels = {o.label for o in filtered}
        assert labels == {"person", "dog"}

    def test_filter_by_labels(self) -> None:
        objs = self._make_objects()
        filtered = DetectionService.filter_by_labels(objs, {"car", "dog"})
        assert len(filtered) == 2

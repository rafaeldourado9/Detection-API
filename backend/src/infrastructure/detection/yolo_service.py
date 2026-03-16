from __future__ import annotations

from ultralytics import YOLO

from src.config import settings
from src.domain.detection.value_objects import BoundingBox, Confidence, DetectedObject

_model: YOLO | None = None


def _get_model() -> YOLO:
    global _model
    if _model is None:
        _model = YOLO(settings.yolo_model_path)
    return _model


def run_inference(image_path: str) -> list[DetectedObject]:
    model = _get_model()
    results = model(image_path, verbose=False)
    detected: list[DetectedObject] = []

    for result in results:
        for box in result.boxes:
            coords = box.xyxy[0].tolist()
            detected.append(
                DetectedObject(
                    label=result.names[int(box.cls[0])],
                    confidence=Confidence(float(box.conf[0])),
                    bbox=BoundingBox(
                        x_min=coords[0],
                        y_min=coords[1],
                        x_max=coords[2],
                        y_max=coords[3],
                    ),
                )
            )

    return detected

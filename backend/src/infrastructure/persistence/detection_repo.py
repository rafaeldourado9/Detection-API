from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.detection.entities import Detection
from src.domain.detection.repository import DetectionRepository
from src.domain.detection.value_objects import (
    BoundingBox,
    Confidence,
    DetectedObject,
    DetectionStatus,
    ImageRef,
)
from src.infrastructure.persistence.models import DetectionModel


class SqlAlchemyDetectionRepository(DetectionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, detection: Detection) -> None:
        existing = await self._session.get(DetectionModel, detection.id)
        if existing:
            existing.status = detection.status
            existing.objects = self._serialize_objects(detection.objects)
            existing.finished_at = detection.finished_at
        else:
            model = DetectionModel(
                id=detection.id,
                user_id=detection.user_id,
                image_path=detection.image.path,
                status=detection.status,
                objects=self._serialize_objects(detection.objects),
                created_at=detection.created_at,
                finished_at=detection.finished_at,
            )
            self._session.add(model)
        await self._session.flush()

    async def find_by_id(self, detection_id: uuid.UUID) -> Detection | None:
        model = await self._session.get(DetectionModel, detection_id)
        return self._to_entity(model) if model else None

    async def list_by_user(
        self, user_id: uuid.UUID, limit: int = 50, offset: int = 0
    ) -> list[Detection]:
        stmt = (
            select(DetectionModel)
            .where(DetectionModel.user_id == user_id)
            .order_by(DetectionModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()]

    @staticmethod
    def _serialize_objects(objects: list[DetectedObject]) -> list[dict] | None:
        if not objects:
            return None
        return [
            {
                "label": o.label,
                "confidence": o.confidence.value,
                "bbox": {
                    "x_min": o.bbox.x_min,
                    "y_min": o.bbox.y_min,
                    "x_max": o.bbox.x_max,
                    "y_max": o.bbox.y_max,
                },
            }
            for o in objects
        ]

    @staticmethod
    def _to_entity(model: DetectionModel) -> Detection:
        objects: list[DetectedObject] = []
        if model.objects:
            for o in model.objects:
                objects.append(
                    DetectedObject(
                        label=o["label"],
                        confidence=Confidence(o["confidence"]),
                        bbox=BoundingBox(**o["bbox"]),
                    )
                )

        created = model.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=UTC)

        finished = model.finished_at
        if finished and finished.tzinfo is None:
            finished = finished.replace(tzinfo=UTC)

        return Detection(
            id=model.id,
            user_id=model.user_id,
            image=ImageRef(model.image_path),
            status=model.status if isinstance(model.status, DetectionStatus) else DetectionStatus(model.status),
            objects=objects,
            created_at=created,
            finished_at=finished,
        )

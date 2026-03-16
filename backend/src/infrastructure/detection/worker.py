from __future__ import annotations

import logging
import uuid

from arq import cron  # noqa: F401

from arq.connections import RedisSettings

from src.config import settings
from src.domain.detection.services import DetectionService
from src.infrastructure.detection.yolo_service import run_inference
from src.infrastructure.persistence.database import async_session
from src.infrastructure.persistence.detection_repo import SqlAlchemyDetectionRepository

logger = logging.getLogger(__name__)


async def run_detection(ctx: dict, detection_id: str) -> None:  # noqa: ARG001
    async with async_session() as session:
        repo = SqlAlchemyDetectionRepository(session)
        detection = await repo.find_by_id(uuid.UUID(detection_id))

        if not detection:
            logger.error("Detection %s not found", detection_id)
            return

        detection.mark_processing()
        await repo.save(detection)
        await session.commit()

        try:
            raw_objects = run_inference(detection.image.path)
            filtered = DetectionService.filter_by_confidence(raw_objects, min_confidence=0.5)
            detection.complete(filtered)
        except Exception:
            logger.exception("Detection %s failed", detection_id)
            detection.fail()

        await repo.save(detection)
        await session.commit()


def _parse_redis_settings() -> RedisSettings:
    from urllib.parse import urlparse
    parsed = urlparse(settings.redis_url)
    return RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
    )


class WorkerSettings:
    functions = [run_detection]
    redis_settings = _parse_redis_settings()

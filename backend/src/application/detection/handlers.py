from __future__ import annotations

from arq import ArqRedis

from src.application.detection.commands import (
    GetDetectionQuery,
    ListDetectionsQuery,
    SubmitDetectionCommand,
)
from src.domain.detection.entities import Detection
from src.domain.detection.exceptions import DetectionNotFoundError
from src.domain.detection.repository import DetectionRepository


class SubmitDetectionHandler:
    def __init__(self, detection_repo: DetectionRepository, redis: ArqRedis) -> None:
        self._repo = detection_repo
        self._redis = redis

    async def handle(self, command: SubmitDetectionCommand) -> Detection:
        detection = Detection.create(
            image_path=command.image_path, user_id=command.user_id
        )
        await self._repo.save(detection)
        await self._redis.enqueue_job("run_detection", str(detection.id))
        return detection


class GetDetectionHandler:
    def __init__(self, detection_repo: DetectionRepository) -> None:
        self._repo = detection_repo

    async def handle(self, query: GetDetectionQuery) -> Detection:
        detection = await self._repo.find_by_id(query.detection_id)
        if not detection:
            raise DetectionNotFoundError(str(query.detection_id))
        return detection


class ListDetectionsHandler:
    def __init__(self, detection_repo: DetectionRepository) -> None:
        self._repo = detection_repo

    async def handle(self, query: ListDetectionsQuery) -> list[Detection]:
        return await self._repo.list_by_user(
            query.user_id, query.limit, query.offset
        )

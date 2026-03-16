from __future__ import annotations

import uuid
from unittest.mock import AsyncMock

import pytest

from src.application.detection.commands import GetDetectionQuery, SubmitDetectionCommand
from src.application.detection.handlers import GetDetectionHandler, SubmitDetectionHandler
from src.domain.detection.entities import Detection
from src.domain.detection.exceptions import DetectionNotFoundError


@pytest.fixture
def detection_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def arq_redis() -> AsyncMock:
    return AsyncMock()


class TestSubmitDetectionHandler:
    async def test_submit_creates_and_enqueues(
        self, detection_repo: AsyncMock, arq_redis: AsyncMock
    ) -> None:
        handler = SubmitDetectionHandler(detection_repo, arq_redis)
        cmd = SubmitDetectionCommand(image_path="/img.jpg", user_id=uuid.uuid4())
        detection = await handler.handle(cmd)
        assert detection.image.path == "/img.jpg"
        detection_repo.save.assert_awaited_once()
        arq_redis.enqueue_job.assert_awaited_once()


class TestGetDetectionHandler:
    async def test_get_existing(self, detection_repo: AsyncMock) -> None:
        uid = uuid.uuid4()
        det = Detection.create("/img.jpg", uid)
        detection_repo.find_by_id.return_value = det
        handler = GetDetectionHandler(detection_repo)
        result = await handler.handle(GetDetectionQuery(detection_id=det.id))
        assert result.id == det.id

    async def test_get_not_found_raises(self, detection_repo: AsyncMock) -> None:
        detection_repo.find_by_id.return_value = None
        handler = GetDetectionHandler(detection_repo)
        with pytest.raises(DetectionNotFoundError):
            await handler.handle(GetDetectionQuery(detection_id=uuid.uuid4()))

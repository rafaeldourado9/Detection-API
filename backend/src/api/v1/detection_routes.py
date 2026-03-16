from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, status

from src.api.dependencies import CurrentUserId, DbSession
from src.api.schemas import BBoxResponse, DetectedObjectResponse, DetectionResponse
from src.application.detection.commands import (
    GetDetectionQuery,
    ListDetectionsQuery,
    SubmitDetectionCommand,
)
from src.application.detection.handlers import (
    GetDetectionHandler,
    ListDetectionsHandler,
    SubmitDetectionHandler,
)
from src.domain.detection.entities import Detection
from src.domain.detection.exceptions import DetectionNotFoundError
from src.infrastructure.persistence.detection_repo import SqlAlchemyDetectionRepository
from src.infrastructure.redis import get_arq_redis

router = APIRouter()

UPLOAD_DIR = Path("/app/uploads")


def _to_response(detection: Detection) -> DetectionResponse:
    objects = None
    if detection.objects:
        objects = [
            DetectedObjectResponse(
                label=o.label,
                confidence=o.confidence.value,
                bbox=BBoxResponse(
                    x_min=o.bbox.x_min,
                    y_min=o.bbox.y_min,
                    x_max=o.bbox.x_max,
                    y_max=o.bbox.y_max,
                ),
            )
            for o in detection.objects
        ]
    return DetectionResponse(
        id=detection.id,
        status=detection.status.value,
        image_path=detection.image.path,
        objects=objects,
        created_at=detection.created_at,
        finished_at=detection.finished_at,
    )


@router.post("", response_model=DetectionResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_detection(
    file: UploadFile,
    session: DbSession,
    user_id: CurrentUserId,
) -> DetectionResponse:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    dest = UPLOAD_DIR / filename
    with dest.open("wb") as buf:
        shutil.copyfileobj(file.file, buf)

    repo = SqlAlchemyDetectionRepository(session)
    arq = await get_arq_redis()
    handler = SubmitDetectionHandler(repo, arq)
    detection = await handler.handle(SubmitDetectionCommand(image_path=str(dest), user_id=user_id))
    return _to_response(detection)


@router.get("/{detection_id}", response_model=DetectionResponse)
async def get_detection(
    detection_id: uuid.UUID,
    session: DbSession,
    user_id: CurrentUserId,  # noqa: ARG001
) -> DetectionResponse:
    repo = SqlAlchemyDetectionRepository(session)
    handler = GetDetectionHandler(repo)
    try:
        detection = await handler.handle(GetDetectionQuery(detection_id=detection_id))
    except DetectionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detection not found")
    return _to_response(detection)


@router.get("", response_model=list[DetectionResponse])
async def list_detections(
    session: DbSession,
    user_id: CurrentUserId,
    limit: int = 50,
    offset: int = 0,
) -> list[DetectionResponse]:
    repo = SqlAlchemyDetectionRepository(session)
    handler = ListDetectionsHandler(repo)
    detections = await handler.handle(ListDetectionsQuery(user_id=user_id, limit=limit, offset=offset))
    return [_to_response(d) for d in detections]

import uuid
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status

from src.api.dependencies import DbSession, CurrentUser
from src.api.schemas import CreateCameraRequest, CameraResponse
from src.application.camera.commands import CreateCameraCommand, StartCameraCommand, StopCameraCommand
from src.application.camera.handlers import CreateCameraHandler, StartCameraHandler, StopCameraHandler
from src.domain.camera.value_objects import CameraType
from src.infrastructure.persistence.camera_repo import SqlAlchemyCameraRepository

router = APIRouter()


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def create_camera(body: CreateCameraRequest, session: DbSession, user: CurrentUser) -> CameraResponse:
    repo = SqlAlchemyCameraRepository(session)
    handler = CreateCameraHandler(repo)
    camera = await handler.handle(
        CreateCameraCommand(
            user_id=user.id,
            name=body.name,
            url=body.url,
            camera_type=CameraType(body.camera_type),
        )
    )
    return CameraResponse(
        id=camera.id,
        name=camera.name,
        url=camera.url,
        camera_type=camera.camera_type.value,
        status=camera.status.value,
        created_at=camera.created_at,
        last_detection_at=camera.last_detection_at,
    )


@router.get("", response_model=list[CameraResponse])
async def list_cameras(session: DbSession, user: CurrentUser) -> list[CameraResponse]:
    repo = SqlAlchemyCameraRepository(session)
    cameras = await repo.find_by_user(user.id)
    return [
        CameraResponse(
            id=c.id,
            name=c.name,
            url=c.url,
            camera_type=c.camera_type.value,
            status=c.status.value,
            created_at=c.created_at,
            last_detection_at=c.last_detection_at,
        )
        for c in cameras
    ]


@router.post("/{camera_id}/start", response_model=CameraResponse)
async def start_camera(camera_id: uuid.UUID, session: DbSession, user: CurrentUser) -> CameraResponse:
    repo = SqlAlchemyCameraRepository(session)
    handler = StartCameraHandler(repo)
    camera = await handler.handle(StartCameraCommand(camera_id=camera_id))
    if camera.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return CameraResponse(
        id=camera.id,
        name=camera.name,
        url=camera.url,
        camera_type=camera.camera_type.value,
        status=camera.status.value,
        created_at=camera.created_at,
        last_detection_at=camera.last_detection_at,
    )


@router.post("/{camera_id}/stop", response_model=CameraResponse)
async def stop_camera(camera_id: uuid.UUID, session: DbSession, user: CurrentUser) -> CameraResponse:
    repo = SqlAlchemyCameraRepository(session)
    handler = StopCameraHandler(repo)
    camera = await handler.handle(StopCameraCommand(camera_id=camera_id))
    if camera.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return CameraResponse(
        id=camera.id,
        name=camera.name,
        url=camera.url,
        camera_type=camera.camera_type.value,
        status=camera.status.value,
        created_at=camera.created_at,
        last_detection_at=camera.last_detection_at,
    )


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(camera_id: uuid.UUID, session: DbSession, user: CurrentUser) -> None:
    repo = SqlAlchemyCameraRepository(session)
    camera = await repo.find_by_id(camera_id)
    if not camera or camera.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await repo.delete(camera_id)


@router.websocket("/{camera_id}/stream")
async def camera_stream(websocket: WebSocket, camera_id: uuid.UUID) -> None:
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"camera_id": str(camera_id), "status": "processing"})
    except WebSocketDisconnect:
        pass

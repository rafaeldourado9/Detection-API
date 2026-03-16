from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool


class CreateCameraRequest(BaseModel):
    name: str
    url: str
    camera_type: str


class CameraResponse(BaseModel):
    id: UUID
    name: str
    url: str
    camera_type: str
    status: str
    created_at: datetime
    last_detection_at: datetime | None = None


class DetectionResponse(BaseModel):
    id: UUID
    status: str
    image_path: str
    objects: list[DetectedObjectResponse] | None = None
    created_at: datetime
    finished_at: datetime | None = None


class DetectedObjectResponse(BaseModel):
    label: str
    confidence: float
    bbox: BBoxResponse


class BBoxResponse(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float


# Rebuild DetectionResponse now that DetectedObjectResponse is defined
DetectionResponse.model_rebuild()

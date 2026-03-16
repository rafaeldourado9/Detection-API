from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SubmitDetectionCommand:
    image_path: str
    user_id: UUID


@dataclass(frozen=True)
class GetDetectionQuery:
    detection_id: UUID


@dataclass(frozen=True)
class ListDetectionsQuery:
    user_id: UUID
    limit: int = 50
    offset: int = 0

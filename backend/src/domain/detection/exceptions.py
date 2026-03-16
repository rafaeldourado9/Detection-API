class DetectionNotFoundError(Exception):
    def __init__(self, detection_id: str) -> None:
        super().__init__(f"Detection {detection_id} not found")


class DetectionProcessingError(Exception):
    pass

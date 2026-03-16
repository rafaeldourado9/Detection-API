from enum import Enum


class CameraStatus(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    ERROR = "ERROR"


class CameraType(str, Enum):
    RTSP = "RTSP"
    HTTP = "HTTP"
    WEBCAM = "WEBCAM"

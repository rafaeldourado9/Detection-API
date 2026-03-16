import asyncio
import cv2
import numpy as np
from typing import AsyncGenerator

from src.infrastructure.detection.yolo_service import YOLOService


class CameraStreamService:
    def __init__(self, yolo_service: YOLOService) -> None:
        self._yolo = yolo_service

    async def stream_camera(self, camera_url: str) -> AsyncGenerator[tuple[np.ndarray, list], None]:
        cap = cv2.VideoCapture(camera_url)
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Processa frame com YOLO
                detections = await asyncio.to_thread(self._yolo.detect, frame)
                
                yield frame, detections
                
                await asyncio.sleep(0.033)  # ~30 FPS
        finally:
            cap.release()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/detections"
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    yolo_model_path: str = "/app/models/yolov8n.pt"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

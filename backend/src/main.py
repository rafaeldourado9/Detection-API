from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.auth_routes import router as auth_router
from src.api.v1.detection_routes import router as detection_router


def create_app() -> FastAPI:
    application = FastAPI(title="Detection API", version="0.1.0")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    application.include_router(detection_router, prefix="/api/v1/detections", tags=["detections"])

    return application


app = create_app()

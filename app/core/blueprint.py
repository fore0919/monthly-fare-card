from fastapi import FastAPI

from app.api.etc import etc_router
from app.api.v1 import v1_router


def register_router(application: FastAPI) -> None:
    application.include_router(etc_router)
    application.include_router(v1_router)

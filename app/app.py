from fastapi import Depends, FastAPI

from app.core.blueprint import register_router
from app.core.config import settings
from app.core.cors import add_cors
from app.core.docs import description, tags_metadata
from app.core.errorhandler import register_exception_handlers
from app.modules.request import log_request


def create_application() -> FastAPI:
    app_env = settings.APP_ENV
    print(f"env: {app_env}\n ")
    application = FastAPI(
        description=description,
        title=settings.PROJECT_NAME,
        openapi_url="/openapi.json",
        redoc_url="/redocs",
        docs_url="/docs",
        openapi_tags=tags_metadata,  # type: ignore
        version="0.0.1",
    )
    add_cors(application)
    register_router(application)
    register_exception_handlers(application)
    return application


app = create_application()

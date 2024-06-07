import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.exception import BaseException, NotOKResponseError


def register_exception_handlers(application: "FastAPI"):
    application.add_exception_handler(BaseException, exception_handler)

    application.add_exception_handler(
        NotOKResponseError, not_ok_response_exception_handler
    )
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(Exception, generic_exception_handler)


def exception_handler(request: Request, exc: BaseException):
    error = serialize_error_message(exc)
    return JSONResponse(
        status_code=exc.code,
        content={**error},
    )


async def not_ok_response_exception_handler(
    request: Request, exc: NotOKResponseError
):
    return exception_handler(request, exc)


async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.detail == "Not Found":
        exc.__class__.__name__ = "NotFound"
    exc.error_no = None
    exc.code = exc.status_code
    exc.message = exc.detail

    return exception_handler(request, exc)


async def generic_exception_handler(request: Request, exc: Exception):
    exc.code = 500
    exc.message = "Unhandled Error"
    return exception_handler(request, exc)


def serialize_error_message(exc: Exception) -> dict:
    error = {
        "success": False,
        "error_name": exc.__class__.__name__,
        "error_no": getattr(exc, "error_no", None),
        "error_message": getattr(exc, "message", "Unhandled Error"),
        "additional_data": getattr(exc, "additional_data", None),
    }
    if settings.APP_ENV not in ["prod"]:
        error["traceback"] = traceback.format_exc()
    return error

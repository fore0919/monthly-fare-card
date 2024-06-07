from fastapi import APIRouter

from .test import test_router

etc_router = APIRouter()
etc_router.include_router(test_router, tags=["test"], include_in_schema=False)

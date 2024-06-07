from fastapi import APIRouter

from .test import test_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(test_router, tags=["[v1] test"])

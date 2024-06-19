from fastapi import APIRouter

from .card import card_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(card_router, tags=["[v1] Best Card"])

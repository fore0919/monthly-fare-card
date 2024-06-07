from fastapi import APIRouter

test_router = APIRouter()


@test_router.get("/healthz")
def health_check() -> dict[str, bool]:
    return {"success": True}

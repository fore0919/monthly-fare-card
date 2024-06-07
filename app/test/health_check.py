from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"success": True}

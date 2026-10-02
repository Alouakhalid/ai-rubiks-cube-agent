import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}


def test_cube_api_flow():
    state_res = client.get("/api/v1/cube/state")
    assert state_res.status_code == 200
    assert state_res.json()["is_solved"]

    move_res = client.post("/api/v1/cube/move", json={"move": "R"})
    assert move_res.status_code == 200
    assert not move_res.json()["is_solved"]

    reset_res = client.post("/api/v1/cube/reset")
    assert reset_res.status_code == 200
    assert reset_res.json()["is_solved"]

    scramble_res = client.post("/api/v1/cube/scramble", json={"length": 10})
    assert scramble_res.status_code == 200
    assert len(scramble_res.json()["scramble"]) == 10


def test_knowledge_rag_endpoint():
    res = client.get("/api/v1/cube/knowledge?q=Fridrich")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] > 0

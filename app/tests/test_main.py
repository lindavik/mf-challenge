from fastapi.testclient import TestClient

from app.main import app, startup_event

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_nonexistent_endpoint():
    response = client.get("/potato")
    assert response.status_code == 404


def test_mission_endpoint_wrong_method():
    response = client.get("/v1/mission-success/")
    assert response.status_code == 405


def test_mission_endpoint():
    startup_event()
    payload = {
        "countdown": 6,
        "bounty_hunters": [
            {"planet": "Tatooine", "day": 4},
            {"planet": "Dagobah", "day": 5}
        ]
    }
    response = client.post("/v1/mission-success/", json=payload)
    assert response.status_code == 200

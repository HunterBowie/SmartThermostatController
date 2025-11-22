from flask.testing import FlaskClient
import pytest


@pytest.fixture()
def event() -> dict:
    return {
        "start_time": "2025-12-16T09:49:00",
        "end_time": "2025-12-16T09:50:00",
        "target": 25.0
    }

def test_get_temp_ok(client: FlaskClient):
    response = client.get("/get_temp")
    assert response.status_code == 200

def test_get_target_temp_ok(client: FlaskClient):
    response = client.get("/get_target_temp")
    assert response.status_code == 200

def test_set_target_temp_ok(client: FlaskClient):
    response = client.post("/set_target_temp", json={"target": 32.1})
    assert response.status_code == 200

def test_schedule_event_ok(client: FlaskClient, event: dict):
    response = client.post("/schedule_event", json=event)
    assert response.status_code == 200

def test_clear_schedule_ok(client: FlaskClient):
    response = client.post("/clear_schedule")
    assert response.status_code == 200

def test_get_next_event_ok(client: FlaskClient, event: dict):
    client.post("/schedule_event", json=event)
    response = client.get("/get_next_event")
    assert response.status_code == 200


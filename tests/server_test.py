from flask.testing import FlaskClient

def test_get_temp_ok(client: FlaskClient):
    response = client.get("/get_temp")
    assert response.status_code == 200

def test_get_target_temp_ok(client: FlaskClient):
    response = client.get("/get_target_temp")
    assert response.status_code == 200

def test_set_target_temp_ok(client: FlaskClient):
    response = client.post("/set_target_temp", json={"target": 32.1})
    assert response.status_code == 200

def test_add_schedule_slot_ok(client: FlaskClient, slot: dict):
    response = client.post("/add_schedule_slot", json=slot)
    assert response.status_code == 200

def test_clear_schedule_ok(client: FlaskClient):
    response = client.post("/clear_schedule")
    assert response.status_code == 200

def test_get_schedule_ok(client: FlaskClient):
    response = client.get("/get_schedule")
    assert response.status_code == 200


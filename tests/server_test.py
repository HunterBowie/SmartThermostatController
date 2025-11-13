import pytest
from flask.testing import FlaskClient

def test_endpoints_ok(client: FlaskClient):
    response = client.get("/get_temp")
    assert response.status_code == 200
    response = client.get("/get_target_temp")
    assert response.status_code == 200

def test_get_temp(client: FlaskClient):
    response = client.get("/get_temp")
    assert response.json["temp"] == 25.0

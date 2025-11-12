import pytest
from flask.testing import FlaskClient

def test_endpoints_ok(client: FlaskClient):
    response = client.get("/getTemp")
    assert response.status_code == 200
    response = client.get("/getTargetTemp")
    assert response.status_code == 200

def test_get_temp(client: FlaskClient):
    response = client.get("/getTemp")
    assert response.json["temp"] == 25.0
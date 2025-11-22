from flask.testing import FlaskClient
import time


def test_get_temp_testing_value(client: FlaskClient):
    response = client.get("/get_temp")
    assert response.json["temp"] == 25.0

def test_set_temp_get_temp(client: FlaskClient):
    assert client.get("/get_target_temp").json["target"] == None

    client.post("/set_target_temp", json={"target": 26.4})

    time.sleep(0.1)

    assert client.get("/get_target_temp").json["target"] == 26.4




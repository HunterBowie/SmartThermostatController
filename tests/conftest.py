import pytest
from smart_thermostat_controller import create_app, stop_threads
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

@pytest.fixture()
def app() -> Flask:
    app = create_app(testing=True)
    app.config.update({
        "TESTING": True,
    })

    yield app

    stop_threads(app.config["threads"], app.config["stop_event"])


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()

@pytest.fixture()
def slot() -> dict:
    return {
        "start_time": "2025-12-16T09:49:00",
        "end_time": "2025-12-16T09:50:00",
        "target": 25.0
    }
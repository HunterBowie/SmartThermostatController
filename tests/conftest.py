import pytest
from smart_thermostat_controller import create_app
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

@pytest.fixture()
def app() -> Flask:
    app = create_app(testing=True)
    app.config.update({
        "TESTING": True,
    })

    return app


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()
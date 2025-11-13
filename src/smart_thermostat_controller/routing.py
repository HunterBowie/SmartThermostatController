"""
This module contains all the flask routing functions.
"""

from flask import Blueprint, render_template, jsonify, current_app, request

from .hardware import init_hardware, read_temp, heater_on, heater_off
from .thermostat import Thermostat
import logging

bp = Blueprint("main", __name__)

def get_thermostat() -> Thermostat:
    return current_app.config["thermostat"]

@bp.route("/")
def index():
    return "<h1>Hello, Flask! But wait Its not OVER</h1>"

@bp.route("/get_temp")
def get_temp():
    return jsonify(temp=get_thermostat().get_temp()), 200

@bp.route("/set_target_temp", methods=["POST"])
def set_target_temp():
    data: dict = request.get_json()
    if not "target" in data or type(data["target"]) not in [float, int]:
        return jsonify({"error": "Missing or incorrect target value"}), 400

    t = get_thermostat()
    logging.info(f"Setting target, id of t is {id(t)}")
    
    t.set_target(data["target"])

    return "", 200

@bp.route("/get_target_temp")
def get_target_temp():
    t = get_thermostat()
    logging.info(f"Getting target, id of t is {id(t)}")
    return jsonify(target=t.get_target()), 200



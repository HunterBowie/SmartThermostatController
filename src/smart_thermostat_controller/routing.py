"""
This module contains all the flask routing functions.
"""

from flask import Blueprint, jsonify, current_app, request

from smart_thermostat_controller.schedule import Event

from .hardware import init_hardware, read_temp
from .thermostat import Thermostat
import logging
from datetime import datetime

bp = Blueprint("main", __name__)

def get_thermostat() -> Thermostat:
    return current_app.config["thermostat"]

@bp.route("/get_temp")
def get_temp():
    return jsonify(temp=get_thermostat().get_temp()), 200

@bp.route("/get_target_temp")
def get_target_temp():
    t = get_thermostat()
    return jsonify(target=t.get_target()), 200

@bp.route("/set_target_temp", methods=["POST"])
def set_target_temp():
    data: dict = request.get_json()
    if not "target" in data or (data["target"] is not None and type(data["target"]) not in [float, int]):
        return jsonify({"error": "Missing or incorrect target value"}), 400

    t = get_thermostat()
    
    t.set_target(data["target"])

    return "", 200


@bp.route("/schedule_event", methods=["POST"])
def schedule_event():
    t = get_thermostat()
    data: dict = request.get_json()

    event = Event(
        start_time=datetime.fromisoformat(data["start_time"]),
        end_time=datetime.fromisoformat(data["end_time"]),
        target=round(float(data["target"]), 1)
    )

    t.schedule_event(event)
    return "", 200

@bp.route("/clear_schedule", methods=["POST"])
def clear_schedule():
    t = get_thermostat()
    t.clear_schedule()
    return "", 200


@bp.route("/get_next_event")
def get_next_event():
    t = get_thermostat()
    event = t.get_next_event()
    if event is None:
        return jsonify(event=None), 200
    return jsonify(event=event.json()), 200
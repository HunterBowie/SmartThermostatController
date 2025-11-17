"""
This module contains all the flask routing functions.
"""

from flask import Blueprint, jsonify, current_app, request

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
    if not "target" in data or type(data["target"]) not in [float, int, None]:
        return jsonify({"error": "Missing or incorrect target value"}), 400

    t = get_thermostat()
    
    t.set_target(data["target"])

    return "", 200


@bp.route("/add_schedule_slot", methods=["POST"])
def add_schedule_slot():
    t = get_thermostat()
    data: dict = request.get_json()

    try:
        slot = {
            "start_time": datetime.fromisoformat(data["start_time"]),
            "end_time": datetime.fromisoformat(data["end_time"]),
            "target": round(float(data["target"]), 1)
        }

        t.add_schedule_slot(slot)
        return "", 200
    
    except (KeyError, ValueError) as error:
        logging.warning("Bad request made for schedule slot")
        return jsonify({"error": str(error)}), 400

@bp.route("/clear_schedule", methods=["POST"])
def clear_schedule():
    t = get_thermostat()
    t.clear_schedule()
    return "", 200


@bp.route("/get_schedule")
def get_schedule():
    t = get_thermostat()
    schedule = t.get_schedule()

    json_schedule = []
    for slot in schedule:
        json_schedule.append({
            "target": slot["target"],
            "start_time": datetime.isoformat(slot["start_time"]),
            "end_time": datetime.isoformat(slot["end_time"]),
        })

    return jsonify(schedule=json_schedule), 200
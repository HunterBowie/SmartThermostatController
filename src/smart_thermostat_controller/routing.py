"""
This module contains all the flask routing functions.
"""

from flask import Blueprint, render_template, jsonify, current_app

from .hardware import init_hardware, read_temp, heater_on, heater_off

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """Return a simple homepage."""
    return "<h1>Hello, Flask! But wait Its not OVER</h1>"

@bp.route("/getTemp")
def get_temp():
    return jsonify(temp=read_temp(current_app.testing))

@bp.route("/setTargetTemp", methods=["POST"])
def set_target_temp():
    data = request.get_json()
    print(f"DO LOGGING: also {data}")

@bp.route("/getTargetTemp")
def get_target_temp():
    return jsonify(temp=23.1)



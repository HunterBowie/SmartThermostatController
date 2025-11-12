"""
This module contains all the flask routing functions.
"""

from flask import Blueprint, render_template, jsonify

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """Return a simple homepage."""
    return "<h1>Hello, Flask! But wait Its not OVER</h1>"

@bp.route("/getTemp")
def get_temp():
    return jsonify(temp=30.1)

@bp.route("/setTargetTemp", methods=["POST"])
def set_target_temp():
    data = request.get_json()
    print(f"DO LOGGING: also {data}")

@bp.route("/getTargetTemp")
def get_target_temp():
    return jsonify(temp=23.1)



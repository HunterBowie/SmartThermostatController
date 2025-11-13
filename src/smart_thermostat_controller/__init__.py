from flask import Flask
from .routing import bp
import threading
from .thermostat import Thermostat
import time
import logging

import atexit

def stop_threads(threads: list[threading.Thread], stop_event: threading.Event):
    if stop_event.is_set():
        return
    stop_event.set()
    for thread in threads:
        thread.join(timeout=3)
        if thread.is_alive():
            logging.error("Attempted to shut down but a thread did not end in 3 seconds after stop_event")
    logging.info("Threads were shut down")

def create_app(testing=False) -> Flask:
    """Create and configure the Flask application."""

    logging.basicConfig(
        level = logging.DEBUG,
        format = "{asctime} - {levelname} - {message}",
        style = "{",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )

    logging.info("Flask application created")

    app = Flask(__name__)

    thermostat = Thermostat(testing)

    app.config["SECRET_KEY"] = "dev"  # Use environment variables in production
    app.config["thermostat"] = thermostat

    app.register_blueprint(bp)

    if not testing:
        from .hardware import init_hardware
        init_hardware()


    stop_event = threading.Event()

    app.config["threads"] = []
    app.config["stop_event"] = stop_event
    
    # Clean shutdown terminates threads without interupting
    

    atexit.register(lambda : stop_threads(app.config["threads"], stop_event))

    def run_update_thermostat(thermostat: Thermostat):
        logging.info("Update loop for thermostat has started")
        while not stop_event.is_set():
            thermostat.update()
            time.sleep(1)
        logging.info("Update loop for thermostat has ended")

    logging.info("Update loop thread for thermostat created")
    update_thread = threading.Thread(target = run_update_thermostat, 
                                     args=(thermostat,), daemon=False)
    update_thread.start()

    app.config["threads"].append(update_thread)

    return app




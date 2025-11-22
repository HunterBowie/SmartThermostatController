"""
This module contains all the code that processes the hardware values and stores the state of thermostat.

The functionality of this module should be mostly unit testable.
"""

import threading
import logging
from .hardware import read_temp, turn_heater_off, turn_heater_on, is_heater_on
from datetime import datetime
from .schedule import Event, Schedule

class Thermostat:
    """Repersents the smart thermostat controller."""

    def __init__(self, testing: bool):
        self.lock = threading.Lock()
        self.testing = testing
        self.target: float = None
        self.margin_turn_off = 0 # turn off 0 degrees above target
        self.margin_turn_on = 2 # turn on 2 degrees below target
        self.current_slot: Event = None
        self.schedule = Schedule()
    
    def shut_down(self):
        turn_heater_off(self.testing)
    
    def update(self):
        """
        Updates the heater in response to sensor and target temperature and schedule.
        Updates schedule slots to get rid of ones already passed.
        This is called every second.
        """
        temp = read_temp(self.testing)

        if temp > 32 or temp < 0:
            logging.info("Thermostat: heater has been turned off")
            turn_heater_off(self.testing)
            return
        
        if self.current_slot is not None:
            if datetime.now() > self.current_slot.end_time:
                self.current_slot = None
                self.target = None

        if not self.current_slot:
            if self.schedule.size() > 0 and datetime.now() >= self.schedule.peek().start_time:
                self.current_slot = self.schedule.pop()
                self.target = self.current_slot.target

        if self.target is None:
            if is_heater_on(self.testing):
                logging.info("Thermostat: heater has been turned off")
                turn_heater_off(self.testing)
            return
        
        if temp > self.target + self.margin_turn_off:
            if is_heater_on(self.testing):
                logging.info("Thermostat: heater has been turned off")
                turn_heater_off(self.testing)
        elif temp < self.target - self.margin_turn_on:
            if not is_heater_on(self.testing):
                logging.info("Thermostat: heater has been turned on")
                turn_heater_on(self.testing)
    
    def set_target(self, new_target: float):
        """
        Sets the new target. If there is a schedule slot is currently running, that slot is deleted.
        """
        with self.lock:
            logging.info(f"Thermostat: setting target to {new_target}")
            self.target = new_target

            if self.current_slot is not None:
                self.current_slot = None


    def schedule_event(self, event: Event):
        """
        Adds new slot to the schedule. 
        """

        with self.lock:
            logging.info(f"Thermostat: adding to schedule event={event}")

            self.schedule.insert(event)
    
    def clear_schedule(self):
        with self.lock:
            logging.info("Thermostat: clearing the schedule")
            self.schedule = Schedule()

    def get_next_event(self) -> Event:
        logging.info("Thermostat: getting the schedule")
        return self.schedule.peek()

    def get_target(self) -> float:
        logging.info(f"Thermostat: getting target={self.target}")
        return self.target
    
    def get_temp(self) -> float:
        temp = read_temp(self.testing)
        logging.info(f"Thermostat: getting temperature temp={temp}°C")
        return temp
    
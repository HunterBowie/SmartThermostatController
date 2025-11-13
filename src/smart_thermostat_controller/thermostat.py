"""
This module contains all the code that processes the hardware values and stores the state of thermostat.

The functionality of this module should be mostly unit testable.
"""

import threading
import logging
from .hardware import read_temp, heater_on, heater_off

class Thermostat:
    def __init__(self, testing: bool):
        self.lock = threading.Lock()
        self.testing = testing
        self.target = 20.0
        self.margin_turn_off = 0 # turn off 0 degrees above target
        self.margin_turn_on = 2 # turn on 2 degrees below target
        self.schedule = []
    
    def update(self):
        """
        Updates the heater in response to sensor and target temperature and schedule.
        Updates schedule slots to get rid of ones already passed.
        This is called every second.
        """
        logging.info("Updating the thermostat")
        with self.lock:
            temp = read_temp(self.testing)

            if temp > self.target + self.margin_turn_off:
                heater_off()
            elif temp < self.target - self.margin_turn_on:
                heater_on()
    
    def set_target(self, new_target: float):
        """
        Sets the new target. If there is a schedule slot is currently running, that slot is deleted.
        """
        logging.info(f"Thermostat setting target to {new_target}")
        with self.lock:
            self.target = new_target
            # slot details not implemented

        logging.info(f"Thermostat target has been set to {self.target}")

    def add_schedule_slot(self, slot: dict):
        """
        Adds new slot to the schedule. 
        Throws a ScheduleException if it conflicts with another slot.
        """
        print("ADDING SCHEDULE SLOT")
        with self.lock:
            pass
    
    def get_schedule(self) -> list[dict]:
        print("GETTING SCHEDULE")
        return []

    def get_target(self) -> float:
        return self.target
    
    def get_temp(self) -> float:
        temp = read_temp(self.testing)
        logging.info(f"A temperature of {temp}°C has been observed")
        return temp
    
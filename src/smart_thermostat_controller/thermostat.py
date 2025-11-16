"""
This module contains all the code that processes the hardware values and stores the state of thermostat.

The functionality of this module should be mostly unit testable.
"""

import threading
import logging
from .hardware import read_temp, turn_heater_off, turn_heater_on, is_heater_on
from datetime import datetime

class Thermostat:
    def __init__(self, testing: bool):
        self.lock = threading.Lock()
        self.testing = testing
        self.target = None
        self.margin_turn_off = 0 # turn off 0 degrees above target
        self.margin_turn_on = 2 # turn on 2 degrees below target
        self.current_slot = None
        self.schedule = []
        logging.info("Creating a thermostat object.")
    
    def update(self):
        """
        Updates the heater in response to sensor and target temperature and schedule.
        Updates schedule slots to get rid of ones already passed.
        This is called every second.
        """
        # logging.info("Updating the thermostat")
        temp = read_temp(self.testing)

        if temp > 29:
            logging.info("Heater has been turned off")
            turn_heater_off(self.testing)
        
        if self.current_slot:
            if datetime.now() > self.current_slot["end_time"]:
                self.current_slot = None
                self.target = None

        if not self.current_slot:
            for slot in self.schedule:
                if datetime.now() >= slot["start_time"]:
                    self.current_slot = slot
                    self.schedule.remove(slot)
                    self.target = slot["target"]
                    break

        if not self.target:
            return
        
        if temp > self.target + self.margin_turn_off:
            if is_heater_on(self.testing):
                logging.info("Heater has been turned off")
                turn_heater_off(self.testing)
        elif temp < self.target - self.margin_turn_on:
            if not is_heater_on(self.testing):
                logging.info("Heater has been turned on")
                turn_heater_on(self.testing)
    
    def set_target(self, new_target: float):
        """
        Sets the new target. If there is a schedule slot is currently running, that slot is deleted.
        """
        logging.info(f"Thermostat setting target to {new_target}")
        with self.lock:
            self.target = new_target

            if self.current_slot:
                self.current_slot = None

        logging.info(f"Thermostat target has been set to {self.target}")

    def add_schedule_slot(self, new_slot: dict):
        """
        Adds new slot to the schedule. 
        Throws a ValueError if it conflicts with another slot.
        """
        print("ADDING SCHEDULE SLOT")

        with self.lock:

            new_duration = (new_slot["end_time"] - new_slot["start_time"]).total_seconds()

            for slot in self.schedule:
                duration = (slot["end_time"] - slot["start_time"]).total_seconds()

                smaller = slot
                larger = new_duration
                if duration > new_duration:
                    larger = slot
                    smaller = new_slot
                
                if smaller["start_time"] <= larger["end_time"] and smaller["start_time"] >= larger["start_time"]:
                    raise ValueError("Smaller start time is within other time slot")
                if smaller["end_time"] <= larger["end_time"] and smaller["end_time"] >= larger["start_time"]:
                    raise ValueError("Smaller end time is within other time slot")
            
            self.schedule.append(slot)
    
    def clear_schedule(self):
        with self.lock:
            self.schedule.clear()

    def get_schedule(self) -> list[dict]:
        return self.schedule

    def get_target(self) -> float:
        logging.info(f"Target temperature is {self.target} and returning value")
        return self.target
    
    def get_temp(self) -> float:
        temp = read_temp(self.testing)
        logging.info(f"A temperature of {temp}°C has been observed")
        return temp
    
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

            if self.current_slot:
                self.current_slot = None


    def add_schedule_slot(self, new_slot: dict):
        """
        Adds new slot to the schedule. 
        Throws a ValueError if it conflicts with another slot.
        """

        with self.lock:
            logging.info(f"Thermostat: adding to schedule slot={new_slot}")

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
            
            self.schedule.append(new_slot)
    
    def clear_schedule(self):
        with self.lock:
            logging.info("Thermostat: clearing the schedule")
            self.schedule.clear()

    def get_schedule(self) -> list[dict]:
        logging.info("Thermostat: getting the schedule")
        return self.schedule

    def get_target(self) -> float:
        logging.info(f"Thermostat: getting target={self.target}")
        return self.target
    
    def get_temp(self) -> float:
        temp = read_temp(self.testing)
        logging.info(f"Thermostat: getting temperature temp={temp}°C")
        return temp
    
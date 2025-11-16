"""
This module contains all the functions that directly communicate with the temp sensor and relay.

When testing, nothing will run and dummy values will be returned instead.
"""

from gpiozero import DigitalOutputDevice
import os
import glob
import time
from enum import Enum, auto


class HardwareUnintializedExeption(Exception):
    pass


BASE_DIR = "/sys/bus/w1/devices/"
DEVICE_DIR = ""
DEVICE_FILE = ""


HEATER_PIN = 27

heater = None

def init_hardware():
    """
    Initializes the hardware systems for the thermostat.
    This is never called when testing.
    """

    os.system("modprobe w1-gpio")
    os.system("modprobe w1-therm")

    global DEVICE_DIR, DEVICE_FILE, heater
    
    DEVICE_DIR = glob.glob(BASE_DIR + "28*")[0]
    DEVICE_FILE = DEVICE_DIR + "/w1_slave"

    heater = DigitalOutputDevice(pin=HEATER_PIN)


def read_temp(testing: bool) -> float:
    """
    Returns the current temperature reading to one decimal place.
    Throws a HardwareUnintializedExeption if init_hardware is not called.
    """

    if testing: return 25.0

    def read_temp_raw() -> list[str]:
        f = open(DEVICE_FILE, "r")
        lines = f.readlines()
        f.close()
        return lines
    
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c, 1)  

def turn_heater_on(testing: bool):
    """Turns the heater on. Throws a HardwareUnintializedExeption if init_hardware is not called."""

    if testing: return

    if not heater:
        raise HardwareUnintializedExeption("The hardware has not been initialized.")
    
    heater.on()

def turn_heater_off(testing: bool):
    """Turns the heater off. Throws a HardwareUnintializedExeption if init_hardware is not called."""

    if testing: return

    if not heater:
        raise HardwareUnintializedExeption("The hardware has not been initialized.")
    
    heater.off()


def is_heater_on(testing: bool):
    """Returns true if the heater is on. Throws a HardwareUnintializedExeption if init_hardware is not called."""

    if testing: return

    if not heater:
        raise HardwareUnintializedExeption("The hardware has not been initialized.")
    
    return not heater.active_high
# SmartThermostatController
A Python Flask Server that is deployed to my Raspberry PI that communicates with a temperature sensor and relay to control the heater. This server will allow a web application to control the heat by making api calls.



## API

"/getTemp"
Returns the current temperature.
response = {
    "temp": 29.3
}

"/setTargetTemp"
Sets the target temperature that the thermastat will try to reach.
request = {
    "target": 28.3
}

"/getTargetTemp"
Gets the current target temperature.
response = {
    "target": 18.3 // (or null if no target)
}

"/getMarginTemp"
Returns the margin values for the temperature control. 
response = {
    "turn_off_margin": 0, // the heater will shut off 0 degrees above the target
    "turn_on_margin": 2 // the heater will turn on if it is 2 degrees below the target
}

"/addScheduleSlot"
Adds a scheduled time to run the thermostat at certain settings.
request = {
    "start_time": "2025-11-11T18:32:45" // ISO 8610
    "end_time": "2025-11-11T18:32:45" // ISO 8610
    "target": 15.2
}

"/getSchedule"
Returns all the added schedule slots that have not started yet.
response = {
    "slots": [
        {"start_time": ..., "end_time": ..., "target": ...}
    ]
}

"/clearSchedule"
Clears all the slots in the schedule.


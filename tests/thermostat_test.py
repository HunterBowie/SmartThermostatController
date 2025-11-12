
from smart_thermostat_controller.thermostat import my_function

def test_testable_function():
    assert my_function(2, 3) == 6
    assert my_function(1, 3) == 3
    assert my_function(0, 1) == 0
    assert my_function(-1, 1) == -1

import pytest
from smart_thermostat_controller.schedule import Schedule, Event
from datetime import datetime, timedelta

@pytest.fixture
def schedule() -> Schedule:
    return Schedule()

def test_constructor(schedule: Schedule):
    try:
        schedule.pop()
    except ValueError:
        pass
    else:
        pytest.fail()
    
    try:
        schedule.peek()
    except ValueError:
        pass
    else:
        pytest.fail()
    
def test_insertion_pop(schedule: Schedule):
    e1 = Event(datetime.now(), datetime.now() + timedelta(days=1), 13.3)
    e2 = Event(datetime.now() + timedelta(days=2), datetime.now() + timedelta(days=5), 13.3)
    e3 = Event(datetime.now() + timedelta(days=5, seconds=1), datetime.now() + timedelta(days=10), 13.3)

    schedule.insert(e2)
    schedule.insert(e1)
    schedule.insert(e3)

    output = [e1, e2, e3]

    assert schedule.size() == 3

    while len(output) != 0:
        assert schedule.pop() == output[0]
        output.pop(0)
    
    assert schedule.size() == 0

  
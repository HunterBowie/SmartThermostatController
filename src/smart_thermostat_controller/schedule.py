from dataclasses import dataclass
from datetime import datetime, timezone
import math

@dataclass
class Event:
    """Repersents a scheduled thermostat target temperature event."""
    start_time: datetime
    end_time: datetime
    target: float

    def unix_time(self) -> int:
        return round(self.start_time.replace(tzinfo=timezone.utc).timestamp())

    def json(self) -> dict:
        return {
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "target": round(self.target, 1)
        }
    
    def __str__(self) -> str:
        return f"start: {self.start_time}, end: {self.end_time}, target: {self.target}"


class Schedule:
    """Repersents all the scheduled temperature events for the thermostat.

    This is implemented as a min heap where the elements are ordered using
    Unix time. I did it this way to practice heap concepts in CPSC 221.
    """

    def __init__(self):
        self.events: list[Event] = []

    def _left_child(self, curr_index: int) -> int:
        """Returns the index of the left child of the given event.
        
        Requires the left child to exist.
        """

        return (curr_index * 2) + 1

    def _right_child(self, curr_index: int) -> int:
        """Returns the index of the right child of the given event.
        
        Requires the right child to exist.
        """

        return (curr_index * 2) + 2

    def _has_a_child(self, curr_index: int) -> bool:
        """Return whether the given event has at least one child."""

        return self._left_child(curr_index) < len(self.events)

    def _has_right_child(self, curr_index: int) -> bool:
        """Return whether the given event has a right child."""

        return self._right_child(curr_index) < len(self.events)
    
    def _parent(self, curr_index: int) -> int:
        """Returns the index of the parent of the given event.
        
        Requires the parent to exist."""

        return math.floor((curr_index - 1) / 2)

    def _swap(self, i: int, j: int):
        """Swaps two events in the list."""
        self.events[i], self.events[j] = self.events[j], self.events[i]

    def _heapifyUp(self, curr_index: int):
        """Move the given event up if it is smaller than its parent."""

        if curr_index == 0:
            return
        
        parent_index = self._parent(curr_index)

        if self.events[curr_index].unix_time() < self.events[parent_index].unix_time():
            self._swap(curr_index, parent_index)
            self._heapifyUp(parent_index)

    
    def _heapifyDown(self, curr_index: int):
        """Move the given event down if it is bigger than its children."""

        if not self._has_a_child(curr_index):
            return
        
        left_child_index = self._left_child(curr_index)
        right_child_index = self._right_child(curr_index)

        min_child_index = left_child_index
        if self._has_right_child(curr_index) \
            and self.events[right_child_index].unix_time() < self.events[left_child_index].unix_time():
            min_child_index = right_child_index

        if self.events[min_child_index].unix_time() < self.events[curr_index].unix_time():
            self._swap(curr_index, min_child_index)
            self._heapifyDown(min_child_index)

    def peek(self) -> Event:
        """Returns a copy of the event with the smallest Unix time value."""

        if len(self.events) == 0:
            raise ValueError("There are no events in the schedule.")
        return self.events[0]

    def pop(self) -> Event:
        """Removes and returns a copy of the event with the smallest Unix time value."""

        if len(self.events) == 0:
            raise ValueError("There are no events in the schedule.")
        
        min_event = self.events[0]

        self._swap(0, len(self.events) - 1)
        self.events.pop()

        self._heapifyDown(0)

        return min_event

    def insert(self, event: Event):
        """Inserts the given event into the schedule."""

        self.events.append(event)
        self._heapifyUp(len(self.events) - 1)
    
    def size(self) -> int:
        return len(self.events)
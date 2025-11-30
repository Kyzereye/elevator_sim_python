"""
Timer class for managing time operations (demonstrates composition).
"""

import time
from typing import Union


class Timer:
    """Timer class for managing time operations (demonstrates composition)."""
    
    def __init__(self, real_time: bool = False) -> None:
        self.real_time = real_time
        self.total_elapsed = 0
    
    def sleep(self, duration: float) -> float:
        """Sleep for specified duration (if real_time is True)."""
        if self.real_time:
            time.sleep(duration)
        return duration
    
    @staticmethod
    def calculate_travel_time(floors: int, time_per_floor: int) -> int:
        """
        Calculate travel time for given number of floors.
        
        Static method: This is a utility function that doesn't need instance state.
        It can be called on the class (Timer.calculate_travel_time()) or on an instance.
        """
        return floors * time_per_floor
    
    def get_total_elapsed(self) -> float:
        """Get total elapsed time tracked by timer."""
        return self.total_elapsed
    
    def reset(self) -> None:
        """Reset the timer."""
        self.total_elapsed = 0


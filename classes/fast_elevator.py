"""
Fast Elevator implementation.
"""

from .elevator import Elevator


class FastElevator(Elevator):
    """Fast elevator - travels twice as fast."""
    FLOOR_TRAVEL_TIME = 5  # Override: 5 seconds per floor instead of 10
    
    def run(self):
        """Override: Run simulation with fast elevator announcement."""
        # Show fast elevator message once at the start
        print("Using the express elevator!\n")
        # Call parent method to handle the actual simulation
        return super().run()


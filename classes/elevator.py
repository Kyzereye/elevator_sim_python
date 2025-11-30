"""
Base Elevator class with common behavior.
"""

import time
import logging
import threading
from .timer import Timer
from util import validate_floor, door_control_instructions


class Elevator:
    """Base class for elevators with common behavior."""
    
    # Class constants (timing values in seconds)
    FLOOR_TRAVEL_TIME = 10  # seconds per floor
    DOOR_OPEN_TIME = 2      # seconds to open doors
    DOOR_CLOSE_TIME = 2     # seconds to close doors
    PASSENGER_TRANSFER_TIME = 4  # seconds for passenger transfer
    
    def __init__(self, start_floor, floors_to_visit, real_time=False):
        self._current_floor = None  # Private attribute (will be set via property)
        self.current_floor = start_floor  # Use property setter for validation
        self.floors_to_visit = floors_to_visit
        self.real_time = real_time
        self.total_time = 0
        self.travel_time = 0
        self.door_operation_time = 0
        self.passenger_transfer_time = 0
        self.visited_floors = [start_floor]
        self.close_door_pressed = threading.Event()
        self.stop_listener = threading.Event()
        self.current_state = "idle"  # idle, traveling, doors_open, transferring, doors_closing
        self.skip_passenger_transfer = False
        
        # Composition: Elevator HAS-A Timer
        self.timer = Timer(real_time=real_time)
    
    @property
    def current_floor(self):
        """Getter: Return current floor."""
        return self._current_floor
    
    @current_floor.setter
    def current_floor(self, value):
        """Setter: Set current floor with validation."""
        if not isinstance(value, int):
            raise TypeError(f"Floor must be an integer. Got: {type(value).__name__}")
        validate_floor(value)  # Validate floor is in valid range
        self._current_floor = value
    
    def print_status(self, message):
        """Print status message."""
        print(message)
        if self.real_time:
            self.timer.sleep(0.1)
    
    def keyboard_listener(self):
        """Listen for keyboard input in a separate thread."""
        while not self.stop_listener.is_set():
            try:
                key = input()
                if key == 'c':
                    if self.current_state == "traveling":
                        print("  ⚠ Doors are already closed (elevator is moving)")
                        logging.info("Door close button pressed while traveling - ignored")
                    elif self.current_state in ["doors_open", "transferring"]:
                        self.close_door_pressed.set()
                        logging.info(f"Door close button pressed during {self.current_state}")
                    elif self.current_state == "doors_closing":
                        # Doors are already closing, ignore
                        pass
            except:
                break
    
    def open_doors(self, floor):
        """Open doors at a floor."""
        self.current_state = "doors_open"
        self.print_status(f"The doors are opening on floor {floor}.")
        actual_time = self.DOOR_OPEN_TIME
        if self.real_time:
            actual_time = self._interruptible_sleep(self.DOOR_OPEN_TIME, allow_close_button=True, is_door_opening=True)
        return actual_time
    
    def close_doors(self, floor):
        """Close doors at a floor."""
        # Clear the flag if it was set (door close button was pressed)
        if self.close_door_pressed.is_set():
            self.close_door_pressed.clear()
            logging.info(f"Closing doors on floor {floor} (door close button was pressed)")
        
        # Reset skip flag
        self.skip_passenger_transfer = False
        
        # Doors always take time to close
        self.current_state = "doors_closing"
        self.print_status(f"The doors are closing on floor {floor}.")
        self.timer.sleep(self.DOOR_CLOSE_TIME)
        self.current_state = "idle"
        return self.DOOR_CLOSE_TIME
    
    def _interruptible_sleep(self, duration, allow_close_button=False, is_door_opening=False):
        """Sleep that can be interrupted by door close button. Returns actual time elapsed."""
        elapsed = 0
        step = 0.1  # Check every 100ms
        while elapsed < duration:
            if allow_close_button and self.close_door_pressed.is_set():
                if is_door_opening:
                    # During door opening, skip passenger transfer and keep flag for close_doors
                    print("  → Door close button activated - skipping passenger transfer!")
                    self.skip_passenger_transfer = True
                    logging.info(f"Door opening interrupted after {elapsed:.1f}s - passenger transfer will be skipped")
                else:
                    # During passenger transfer, just skip remaining time
                    print("  → Door close button activated - Closing doors!")
                    logging.info(f"Passenger transfer interrupted after {elapsed:.1f}s by door close button press")
                    self.close_door_pressed.clear()
                return elapsed
            sleep_time = min(step, duration - elapsed)
            time.sleep(sleep_time)
            elapsed += sleep_time
        return duration  # Return full duration if not interrupted
    
    def transfer_passengers(self, floor):
        """Handle passenger transfer."""
        # Check if passenger transfer should be skipped (door close pressed during door opening)
        if self.skip_passenger_transfer:
            self.skip_passenger_transfer = False
            logging.info(f"Skipping passenger transfer on floor {floor}")
            return 0
        
        self.current_state = "transferring"
        self.print_status(f"Passenger transfer on floor {floor}.")
        actual_time = self.PASSENGER_TRANSFER_TIME
        if self.real_time:
            actual_time = self._interruptible_sleep(self.PASSENGER_TRANSFER_TIME, allow_close_button=True)
        return actual_time
    
    def travel_to_floor(self, target_floor):
        """Travel from current floor to target floor."""
        floors_to_travel = abs(target_floor - self.current_floor)
        travel_time = self.timer.calculate_travel_time(floors_to_travel, self.FLOOR_TRAVEL_TIME)
        
        if floors_to_travel > 0:
            if target_floor > self.current_floor:
                direction = "up"
            else:
                direction = "down"
            self.current_state = "traveling"
            self.print_status(f"The elevator is traveling {direction} to floor {target_floor} - {travel_time} sec.")
            self.timer.sleep(travel_time)
        
        return travel_time
    
    def visit_floor(self, target_floor):
        """Complete process of visiting a floor."""
        time_elapsed = 0
        time_elapsed_doors = 0
        time_elapsed_passengers = 0
        time_elapsed_travel = 0
        
        # Travel to floor
        time_elapsed_travel += self.travel_to_floor(target_floor)
        self.current_floor = target_floor
        self.visited_floors.append(target_floor)
        
        # Open doors
        time_elapsed_doors += self.open_doors(target_floor)
        
        # Passenger transfer
        time_elapsed_passengers += self.transfer_passengers(target_floor)
        
        # Close doors
        time_elapsed_doors += self.close_doors(target_floor)

        # total time elapsed
        time_elapsed = time_elapsed_doors + time_elapsed_passengers + time_elapsed_travel
        
        return time_elapsed, time_elapsed_doors, time_elapsed_passengers, time_elapsed_travel
    
    def run(self):
        """Run the simulation."""
        print(f"\n=== Elevator Simulation Starting ===")
        print(f"Starting floor: {self.current_floor}")
        print(f"Floors to visit: {', '.join(map(str, self.floors_to_visit))}\n")
        
        if self.real_time:
            door_control_instructions()
            # Start keyboard listener in a separate thread
            listener_thread = threading.Thread(target=self.keyboard_listener, daemon=True)
            listener_thread.start()
        
        logging.info(f"Simulation running - Start floor: {self.current_floor}, Floors to visit: {self.floors_to_visit}")
        
        for floor in self.floors_to_visit:
            if floor == self.current_floor:
                # Already at this floor.  Get the time for operations on this floor only, 
                # then add to totals.
                logging.info(f"Already at floor {floor} - performing door operations only")
                door_open = self.open_doors(floor)
                passenger_transfer = self.transfer_passengers(floor)
                door_close = self.close_doors(floor)

                self.door_operation_time += door_open + door_close
                self.passenger_transfer_time += passenger_transfer
                self.total_time += door_open + door_close + passenger_transfer
            else:
                logging.info(f"Visiting floor {floor} from floor {self.current_floor}")
                time_elapsed, time_elapsed_doors, time_elapsed_passengers, time_elapsed_travel = self.visit_floor(floor)
                self.travel_time += time_elapsed_travel
                self.door_operation_time += time_elapsed_doors
                self.passenger_transfer_time += time_elapsed_passengers
                self.total_time += time_elapsed
                logging.info(f"Completed floor {floor} - Time elapsed: {time_elapsed}s (Travel: {time_elapsed_travel}s, Doors: {time_elapsed_doors}s, Passengers: {time_elapsed_passengers}s)")
        
        # Stop keyboard listener
        if self.real_time:
            self.stop_listener.set()
        
        return self.total_time, self.visited_floors
    
    def get_stats(self):
        """Return simulation statistics as a dictionary."""
        return {
            'total_time': self.total_time,
            'travel_time': self.travel_time,
            'door_operation_time': self.door_operation_time,
            'passenger_transfer_time': self.passenger_transfer_time,
            'visited_floors': self.visited_floors.copy()
        }


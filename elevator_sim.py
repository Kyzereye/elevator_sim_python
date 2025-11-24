#!/usr/bin/env python3
"""
Elevator Simulation Script
Simulates an elevator with door operations and passenger transfers.
"""

import sys
import time

# Constants
FLOOR_TRAVEL_TIME = 10  # seconds per floor
DOOR_OPEN_TIME = 2      # seconds
DOOR_CLOSE_TIME = 2     # seconds
PASSENGER_TRANSFER_TIME = 4  # seconds
MIN_FLOOR = 1           # bottom floor
MAX_FLOOR = 35          # top floor


class ElevatorSimulator:
    """Simulates elevator movement and operations."""
    
    def __init__(self, start_floor, floors_to_visit, real_time=False):
        self.current_floor = start_floor
        self.floors_to_visit = floors_to_visit
        self.real_time = real_time
        self.total_time = 0
        self.travel_time = 0
        self.door_operation_time = 0
        self.passenger_transfer_time = 0
        self.visited_floors = [start_floor]
    
    def print_status(self, message):
        """Print status message."""
        print(message)
        if self.real_time:
            time.sleep(0.1)
    
    def open_doors(self, floor):
        """Open doors at a floor."""
        self.print_status(f"The doors are opening on floor {floor}.")
        if self.real_time:
            time.sleep(DOOR_OPEN_TIME)
        return DOOR_OPEN_TIME
    
    def close_doors(self, floor):
        """Close doors at a floor."""
        self.print_status(f"The doors are closing on floor {floor}.")
        if self.real_time:
            time.sleep(DOOR_CLOSE_TIME)
        return DOOR_CLOSE_TIME
    
    def transfer_passengers(self, floor):
        """Handle passenger transfer."""
        self.print_status(f"Passenger transfer on floor {floor}.")
        if self.real_time:
            time.sleep(PASSENGER_TRANSFER_TIME)
        return PASSENGER_TRANSFER_TIME
    
    def travel_to_floor(self, target_floor):
        """Travel from current floor to target floor."""
        floors_to_travel = abs(target_floor - self.current_floor)
        travel_time = floors_to_travel * FLOOR_TRAVEL_TIME
        
        if floors_to_travel > 0:
            if target_floor > self.current_floor:
                direction = "up"
            else:
                direction = "down"
            self.print_status(f"The elevator is traveling {direction} to floor {target_floor} - {travel_time} sec.")
            if self.real_time:
                time.sleep(travel_time)
        
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
        
        for floor in self.floors_to_visit:
            if floor == self.current_floor:
                # Already at this floor.  Get the time for operations on this floor only, 
                # then add to totals.
                door_open = self.open_doors(floor)
                passenger_transfer = self.transfer_passengers(floor)
                door_close = self.close_doors(floor)

                self.door_operation_time += door_open + door_close
                self.passenger_transfer_time += passenger_transfer
                self.total_time += door_open + door_close + passenger_transfer
            else:
                time_elapsed, time_elapsed_doors, time_elapsed_passengers, time_elapsed_travel = self.visit_floor(floor)
                self.travel_time += time_elapsed_travel
                self.door_operation_time += time_elapsed_doors
                self.passenger_transfer_time += time_elapsed_passengers
                self.total_time += time_elapsed
        
        print(f"\n=== Simulation Complete ===")
        print(f"Total operations time: {self.total_time} seconds")
        print(f"Total door operations time(open + close): {self.door_operation_time} seconds")
        print(f"Total passenger transfer time: {self.passenger_transfer_time} seconds")
        print(f"Total travel time: {self.travel_time} seconds")
        print(f"Floors visited in order: {','.join(map(str, self.visited_floors))}\n")
        
        return self.total_time, self.visited_floors


def validate_floor(floor):
    """Check if floor is within valid range."""
    if floor < MIN_FLOOR or floor > MAX_FLOOR:
        raise ValueError(f"Floor {floor} is out of range. Valid floors are {MIN_FLOOR} to {MAX_FLOOR}.")


def parse_input(input_str):
    """Parse input string to get start floor and floors to visit."""
    input_str = input_str.strip()
    
    # Format: "start=12 floor=2,9,1,32"
    if "start=" not in input_str or "floor=" not in input_str:
        raise ValueError("Invalid input format. Expected: 'start=X floor=Y,Z,...'")
    
    # Extract start floor value
    start_idx = input_str.find("start=")
    floor_idx = input_str.find("floor=")
    
    # Get the value after "start=" (everything until "floor=" or end)
    if start_idx < floor_idx:
        start_floor_str = input_str[start_idx + 6:floor_idx].strip()  # 6 = len("start=")
    else:
        start_floor_str = input_str[start_idx + 6:].strip()
    
    # Get the value after "floor=" (everything after it)
    floors_str = input_str[floor_idx + 6:].strip()  # 6 = len("floor=")
    
    # Validate and convert start floor
    if not start_floor_str:
        raise ValueError("Start floor cannot be empty. Expected: 'start=X' where X is a number.")
    try:
        start_floor = int(start_floor_str)
    except ValueError:
        raise ValueError(f"Start floor must be a number. Got: '{start_floor_str}'")
    
    # Validate and convert floor list
    if not floors_str:
        raise ValueError("Floor list cannot be empty. Expected: 'floor=Y,Z,...' where Y,Z are numbers.")
    
    floors = []
    for f in floors_str.split(","):
        f_clean = f.strip()
        if not f_clean:  # Skip empty strings between commas
            continue
        try:
            floors.append(int(f_clean))
        except ValueError:
            raise ValueError(f"All floors must be numbers. Got: '{f_clean}'")
    
    if not floors:
        raise ValueError("At least one floor must be specified in the floor list.")
    
    return start_floor, floors


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python3 elevator_sim.py 'start=12 floor=2,9,1,32' [--real-time]")
        print("\nNote: [--real-time] is optional. Do not include the brackets in the command.")
        print("      Use: python3 elevator_sim.py 'start=12 floor=2,9,1,32' --real-time")
        sys.exit(1)
    
    # Check for --real-time flag
    real_time = False
    input_str = sys.argv[1]
    if len(sys.argv) > 2 and "--real-time" in sys.argv:
        real_time = True
    
    try:
        start_floor, floors_to_visit = parse_input(input_str)
        
        # Validate all floors are within range
        validate_floor(start_floor)
        for floor in floors_to_visit:
            validate_floor(floor)
        
        simulator = ElevatorSimulator(start_floor, floors_to_visit, real_time=real_time)
        total_time, visited_floors = simulator.run()
        print(f"OUTPUT: {total_time} {','.join(map(str, visited_floors))}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nSimulation interrupted.")
        sys.exit(1)


if __name__ == "__main__":
    main()

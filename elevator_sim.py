#!/usr/bin/env python3
"""
Elevator Simulation Script
Simulates an elevator with door operations and passenger transfers.
"""

import sys
import logging
from util import parse_input, setup_logging, log_simulation_start, log_simulation_complete, simulation_instructions, validate_floor
from classes import StandardElevator, FastElevator


def main():
    """Main function."""
    # Setup logging to file
    setup_logging()
    
    if len(sys.argv) < 2:
        # Display simulation instructions if no arguments are provided
        simulation_instructions()
        sys.exit(1)
    
    # Check for flags
    real_time = False
    use_fast = False
    input_str = sys.argv[1]
    
    if len(sys.argv) > 2:
        if "--real-time" in sys.argv:
            real_time = True
        if "--fast" in sys.argv:
            use_fast = True
    
    log_simulation_start(input_str, real_time)
    
    try:
        start_floor, floors_to_visit = parse_input(input_str)
        logging.info(f"Parsed input - Start floor: {start_floor}, Floors to visit: {floors_to_visit}")
        
        # Validate all floors are within range
        validate_floor(start_floor)
        for floor in floors_to_visit:
            validate_floor(floor)
        logging.info("All floors validated successfully")
        
        # Create elevator instance (choose type based on flag)
        if use_fast:
            simulator = FastElevator(start_floor, floors_to_visit, real_time=real_time)
            logging.info("Using FastElevator (5 seconds per floor)")
        else:
            simulator = StandardElevator(start_floor, floors_to_visit, real_time=real_time)
            logging.info("Using StandardElevator (10 seconds per floor)")
        
        simulator.run()
        
        # Display statistics
        stats = simulator.get_stats()
        print(f"\n=== Simulation Complete ===")
        print(f"Total Operations Time: {stats['total_time']} seconds")
        print(f"Total Travel Time: {stats['travel_time']} seconds")
        print(f"Total Door Operations Time(open + close): {stats['door_operation_time']} seconds")
        print(f"Total Passenger Transfers Time: {stats['passenger_transfer_time']} seconds")
        print(f"Floors Visited: {','.join(map(str, stats['visited_floors']))}")
        
        # Log statistics
        log_simulation_complete(stats)
        
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        logging.warning("Simulation interrupted by user")
        print("\nSimulation interrupted.")
        sys.exit(1)


if __name__ == "__main__":
    main()

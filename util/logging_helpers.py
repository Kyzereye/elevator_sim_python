"""
Logging helper functions for elevator simulation.
"""

import logging


def setup_logging():
    """Configure logging to output to file."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='elevator_sim.log',
        filemode='a'
    )


def log_simulation_start(input_str, real_time):
    """Log simulation start information."""
    logging.info("=" * 60)
    logging.info("Starting elevator simulation")
    logging.info(f"Input: {input_str}, Real-time mode: {real_time}")


def log_simulation_complete(stats):
    """Log simulation completion with statistics."""
    logging.info("Simulation completed successfully")
    logging.info(f"Statistics - Total Time: {stats['total_time']}s, Travel: {stats['travel_time']}s, "
                 f"Doors: {stats['door_operation_time']}s, Passengers: {stats['passenger_transfer_time']}s")
    logging.info(f"Floors visited: {','.join(map(str, stats['visited_floors']))}")

def simulation_instructions():
    """Output simulation usage instructions."""
    print("Usage: python3 elevator_sim.py 'start=12 floor=2,9,1,32' [--real-time] [--fast]")
    print("\nOptions:")
    print("  --real-time  Enable real-time delays and interactive door control")
    print("  --fast       Use FastElevator (5 sec/floor) instead of StandardElevator (10 sec/floor)")
    print("\nNote: Options are optional. Do not include brackets in the command.")
    print("      Example: python3 elevator_sim.py 'start=12 floor=2,9,1,32' --real-time --fast")
    print("\nLog output is saved to elevator_sim.log")


def door_control_instructions():
    """Output door control instructions."""
    print("Press 'c' + Enter to close doors:")
    print("  - During door opening: skips passenger transfer")
    print("  - During passenger transfer: door closure begins\n")    
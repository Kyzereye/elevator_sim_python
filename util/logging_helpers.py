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


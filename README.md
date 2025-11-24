# Elevator Simulation

A real-time elevator simulation script written in Python that models elevator behavior including travel time, door operations, and passenger transfers.

## Features

- Real-time simulation with status updates
- Interactive door control (press 'c' during door opening or passenger transfer to close doors)
- Accurate time tracking (statistics reflect actual elapsed time, including when operations are interrupted)
- Door opening/closing operations (2 seconds each)
- Passenger transfer time (4 seconds)
- Floor-to-floor travel time (10 seconds per floor)
- Detailed time breakdown (travel time, door operations, passenger transfers)
- Statistics API via `get_stats()` method for programmatic access
- Automatic logging to file (`elevator_sim.log`)
- Threading support for background keyboard listener
- Command-line interface with key-value input format

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Usage

### Basic Usage

```bash
python3 elevator_sim.py "start=12 floor=2,9,1,32"
```

### Real-Time Mode (With Delays)

To run with real-time delays for demonstration:

```bash
python3 elevator_sim.py "start=12 floor=2,9,1,32" --real-time
```

**Interactive Control:** In real-time mode, you can press **`c`** followed by **Enter** while doors are opening or passengers are transferring to activate the door close button. This will:
- **If pressed during door opening**: Skip both remaining door opening time AND passenger transfer, then close doors (doors still take 2 seconds to close)
- **If pressed during passenger transfer**: Skip remaining passenger transfer time, then close doors (doors still take 2 seconds to close)
- **Time tracking**: Statistics accurately reflect actual time spent - if you interrupt an operation, only the elapsed time is counted, not the full duration
- Simulate pressing the close door button in a real elevator
- Alert you if pressed during travel (doors are already closed)
- Note: Door closing always takes its full 2 seconds - what gets skipped is only the door opening and/or passenger transfer

**Note:** All simulation runs are automatically logged to `elevator_sim.log` in the current directory.

### Example Output

```
=== Elevator Simulation Starting ===
Starting floor: 12
Floors to visit: 2, 9, 1, 32

The elevator is traveling down to floor 2.
The doors are opening on floor 2.
Passenger transfer on floor 2.
The doors are closing on floor 2.
The elevator is traveling up to floor 9.
The doors are opening on floor 9.
Passenger transfer on floor 9.
The doors are closing on floor 9.
...

=== Simulation Complete ===
Total Operations Time: 592 seconds
Total Travel Time: 560 seconds
Total Door Operations Time(open + close): 16 seconds
Total Passenger Transfers Time: 16 seconds
Floors Visited: 12,2,9,1,32
```

## Program Constants

- **Single floor travel time**: 10 seconds
- **Door opening time**: 2 seconds
- **Door closing time**: 2 seconds
- **Passenger transfer time**: 4 seconds
- **Minimum floor**: 1 (ground floor, no basement)
- **Maximum floor**: 35

## Assumptions

1. **Elevator starts with doors closed** - The simulation begins with the elevator at the starting floor with doors closed.

2. **Doors must open and close at each stop** - Even if the elevator is already at a floor, doors still open and close for passenger transfer.

3. **Passenger transfer happens at every stop** - Passengers get in/out at each floor visited, taking 4 seconds.

4. **Travel time is linear** - Time to travel between floors is calculated as `abs(destination - current) * 10 seconds`.

5. **Floors are visited in order** - The elevator visits floors in the exact order specified in the input, even if it means backtracking.

6. **No optimization** - The elevator does not optimize the route (e.g., visiting floors in a more efficient order). It follows the exact sequence provided.

7. **Floor limits** - Valid floors are 1 (ground floor) to 35 (top floor). No basement floors. The program will reject any floor outside this range.

## Features Not Implemented

1. **Route optimization** - The elevator doesn't optimize the route to minimize travel time. It visits floors in the exact order specified.

2. **Multiple elevators** - Only a single elevator is simulated.

3. **Elevator capacity** - No limit on number of passengers or weight capacity.

4. **Emergency stops** - No handling of emergency situations or emergency stop buttons.

5. **Door obstruction** - No handling of doors being held open or obstructed.

6. **Concurrent requests** - No handling of new floor requests while the elevator is in motion.

## Testing

Test with the example from the requirements:

```bash
python3 elevator_sim.py "start=12 floor=2,9,1,32"
```

The output will display the simulation status messages as it progresses, followed by a statistics summary showing total time, travel time, door operations time, passenger transfer time, and the floors visited.

## Logging

All simulation runs are automatically logged to `elevator_sim.log` in the same directory. The log file includes:

- Simulation start time and input parameters
- Floor validation results
- Detailed progress for each floor visited
- Time breakdowns for each operation (including actual time when interrupted by door close button)
- Interactive door close button activations with elapsed times
- Final statistics
- Any errors or interruptions

Log entries are appended to the file, so you can track multiple simulation runs over time.

**Example log entry:**
```
2025-11-24 13:26:07 - INFO - Starting elevator simulation
2025-11-24 13:26:07 - INFO - Input: start=12 floor=2,9,1,32, Real-time mode: False
2025-11-24 13:26:07 - INFO - Parsed input - Start floor: 12, Floors to visit: [2, 9, 1, 32]
2025-11-24 13:26:07 - INFO - All floors validated successfully
2025-11-24 13:26:07 - INFO - Visiting floor 2 from floor 12
2025-11-24 13:26:07 - INFO - Completed floor 2 - Time elapsed: 108s (Travel: 100s, Doors: 4s, Passengers: 4s)
...
```

## Programmatic Usage

The `get_stats()` method allows you to use the simulator programmatically:

```python
from elevator_sim import ElevatorSimulator

# Create and run simulation
simulator = ElevatorSimulator(start_floor=12, floors_to_visit=[2, 9, 1, 32], real_time=False)
simulator.run()

# Get statistics as dictionary
stats = simulator.get_stats()
print(f"Total time: {stats['total_time']} seconds")
print(f"Floors visited: {stats['visited_floors']}")

# Access individual metrics
travel_time = stats['travel_time']
door_time = stats['door_operation_time']
passenger_time = stats['passenger_transfer_time']
```

## Project Structure

```
elevator_sim_python/
├── elevator_sim.py          # Main simulation script
├── util/                     # Utility module
│   ├── __init__.py          # Package initialization
│   ├── helpers.py           # Input parsing and validation functions
│   └── logging_helpers.py   # Logging configuration and helper functions
├── elevator_sim.log         # Log file (generated during runtime)
└── README.md                # This file
```

## Code Structure

### Main Components

- **`ElevatorSimulator` class**: Main simulation logic
  - `run()`: Executes the simulation with optional keyboard listener thread
  - `get_stats()`: Returns simulation statistics as a dictionary
  - `visit_floor()`: Handles complete floor visit sequence
  - `travel_to_floor()`: Simulates travel between floors
  - `open_doors()`, `close_doors()`: Door operations with interactive control
  - `transfer_passengers()`: Passenger transfer simulation (can be skipped via door close button)
  - `keyboard_listener()`: Background thread for interactive door control (real-time mode only)
  - `_interruptible_sleep()`: Internal method that allows operations to be interrupted, returns actual elapsed time

- **Helper Functions**:
  - Input/Validation (in `util/helpers.py`):
    - `parse_input()`: Parses command-line input in key-value format
    - `validate_floor()`: Validates floor numbers are within range (1-35)
  - Logging (in `util/logging_helpers.py`):
    - `setup_logging()`: Configures logging system
    - `log_simulation_start()`: Logs simulation start information
    - `log_simulation_complete()`: Logs completion with statistics

- **Main Entry Point**:
  - `main()`: Entry point and command-line interface with logging setup

## License

This project is provided as-is for interview/demonstration purposes.

# Elevator Simulation

A real-time elevator simulation script written in Python that models elevator behavior including travel time, door operations, and passenger transfers.

## Features

- Real-time simulation with status updates
- Door opening/closing operations (2 seconds each)
- Passenger transfer time (4 seconds)
- Floor-to-floor travel time (10 seconds per floor)
- Command-line interface with flexible input formats

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Usage

### Basic Usage

```bash
python3 elevator_sim.py "start=12 floor=2,9,1,32"
```

Or with alternative format:

```bash
python3 elevator_sim.py "12 2,9,1,32"
```

### Fast Mode (No Delays)

To calculate instantly without real-time delays:

```bash
python3 elevator_sim.py "start=12 floor=2,9,1,32" --no-delay
```

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
Total travel time: 560 seconds
Floors visited in order: 12,2,9,1,32

OUTPUT: 560 12,2,9,1,32
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

7. **Starting floor is included in visited floors** - The output includes the starting floor as the first floor in the visited list.

8. **Real-time mode is default** - By default, the simulation runs with real-time delays. Use `--no-delay` flag for instant calculation.

9. **Floor limits** - Valid floors are 1 (ground floor) to 35 (top floor). No basement floors. The program will reject any floor outside this range.

## Features Not Implemented

1. **Route optimization** - The elevator doesn't optimize the route to minimize travel time. It visits floors in the exact order specified.

2. **Multiple elevators** - Only a single elevator is simulated.

3. **Elevator capacity** - No limit on number of passengers or weight capacity.

4. **Emergency stops** - No handling of emergency situations or button presses.

5. **Direction indicators** - No visual indication of which direction the elevator is moving (though it's mentioned in text).

6. **Concurrent requests** - No handling of new floor requests while the elevator is in motion.

8. **Door obstruction** - No handling of doors being held open or obstructed.

## Testing

Test with the example from the requirements:

```bash
python3 elevator_sim.py "start=12 floor=2,9,1,32"
```

Expected output format:
```
OUTPUT: <total_time> <start_floor>,<floor1>,<floor2>,...
```

## Code Structure

- `ElevatorSimulator` class: Main simulation logic
- `parse_input()`: Parses command-line input in multiple formats
- `main()`: Entry point and command-line interface
- Individual simulation methods for each operation (travel, door operations, passenger transfer)

## License

This project is provided as-is for interview/demonstration purposes.

# elevator_sim_python

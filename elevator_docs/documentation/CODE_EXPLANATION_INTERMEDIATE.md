# Code Explanation: Elevator Simulation (Intermediate Level)

This document explains the elevator simulation code structure, logic flow, and design decisions for developers with intermediate Python knowledge.

---

## Overall Architecture

The code is organized into three main parts:
1. **ElevatorSimulator class** - Encapsulates all elevator behavior and state
2. **parse_input function** - Handles command-line input parsing
3. **main function** - Entry point that orchestrates everything

---

## ElevatorSimulator Class

### Purpose
Models an elevator as an object that maintains state (current floor, total time, visited floors) and performs operations (travel, door operations, passenger transfer).

### State Management (`__init__`)
```python
def __init__(self, start_floor, floors_to_visit, real_time=True):
    self.current_floor = start_floor
    self.floors_to_visit = floors_to_visit
    self.real_time = real_time
    self.total_time = 0
    self.travel_time = 0
    self.door_operation_time = 0
    self.passenger_transfer_time = 0
    self.visited_floors = [start_floor]
```

**Key points:**
- `real_time` flag controls whether to use `time.sleep()` for delays or just calculate instantly
- `visited_floors` starts with the starting floor since it's part of the path
- Time tracking is separated into: total, travel, door operations, and passenger transfers
- All state is instance variables, allowing multiple elevator instances if needed

### Operation Methods

**`print_status(message)`**
- Centralized status printing with optional small delay for readability
- Why separate: DRY principle and easy to modify output format later

**`open_doors(floor)` / `close_doors(floor)` / `transfer_passengers(floor)`**
- Each returns the time taken (for time tracking)
- Pattern: print status → sleep if real-time → return time constant
- Why separate methods: Clear separation of concerns, easy to modify behavior independently

**`travel_to_floor(target_floor)`**
- Calculates distance: `abs(target_floor - self.current_floor)`
- Determines direction for status message
- Returns travel time without updating `self.current_floor` (that happens in `visit_floor`)
- Why: Keeps travel logic separate from floor visit orchestration

**`visit_floor(target_floor)`**
- Orchestrates the complete sequence: travel → open → transfer → close
- Updates `self.current_floor` and appends to `visited_floors`
- Tracks time separately for travel, doors, and passenger transfer
- Returns tuple: `(total_time, door_time, passenger_time, travel_time)`
- Why this method: High-level abstraction that encapsulates the full workflow

**`run()`**
- Main simulation loop that processes each floor in `floors_to_visit`
- Handles edge case: if already at requested floor, skip travel
- Unpacks time values from `visit_floor()` and accumulates them separately
- Updates instance variables: `self.travel_time`, `self.door_operation_time`, `self.passenger_transfer_time`, `self.total_time`
- Prints detailed time breakdown at the end
- Returns tuple for use by main function

**Key design decision:** Each operation method returns time taken, allowing time tracking even when delays are disabled (default mode). Time is tracked separately for analysis and reporting.

---

## Input Parsing

### `parse_input(input_str)`

Parses input in key-value format: `"start=12 floor=2,9,1,32"`

**Parsing logic:**
- Checks for `"start="` and `"floor="` substrings (required)
- Splits input on space, then extracts values after `=`
- Uses list comprehension to convert comma-separated string to list of integers

**Error handling:** Raises `ValueError` if input is malformed or missing required keys, which is caught in `main()`.

---

## Main Function

### Flow
1. **Argument validation** - Checks if input provided, shows usage if not
2. **Flag detection** - Checks for `--real-time` flag to enable real-time delays
3. **Input parsing** - Converts string input to structured data
4. **Simulation execution** - Creates simulator instance and runs it
5. **Output formatting** - Prints final results in required format

### Error Handling
- `ValueError`: From `parse_input()` - invalid input format
- `KeyboardInterrupt`: User presses Ctrl+C - graceful exit

**Why try/except:** Prevents crashes on invalid input and provides user-friendly error messages.

### Output Format
```python
print(f"OUTPUT: {total_time} {','.join(map(str, visited_floors))}")
```
- Uses `map(str, ...)` to convert integers to strings
- Joins with commas (no spaces) as per requirements
- Example: `"OUTPUT: 592 12,2,9,1,32"`

---

## Design Decisions

### Why a Class?
- **State management**: Elevator needs to track multiple pieces of state (current floor, time, visited floors)
- **Organization**: Groups related functionality together
- **Extensibility**: Easy to add features (multiple elevators, capacity limits, etc.)

### Why Separate Methods for Each Operation?
- **Single Responsibility Principle**: Each method has one clear purpose
- **Maintainability**: Easy to modify individual operations (e.g., change door timing)
- **Testability**: Can test each operation independently
- **Readability**: Method names clearly describe what they do

### Why Return Time Values?
- Allows time tracking in both instant calculation (default) and real-time modes
- Methods are pure in terms of time calculation (always return the same time)
- Enables time accumulation without duplicating constants

### Why `real_time` Flag?
- **User experience**: Real-time mode is engaging to watch (use `--real-time` flag)
- **Testing/debugging**: Default instant mode allows quick iteration
- **Flexibility**: Same code path works for both modes

### Why `if __name__ == "__main__":`?
- Allows script to be imported as a module without running simulation
- Enables testing and reuse of functions/classes
- Standard Python best practice

---

## Code Flow Example

For input `"start=12 floor=2,9,1,32"`:

1. **main()** receives arguments
2. **parse_input()** extracts: `start_floor=12, floors_to_visit=[2,9,1,32]`
3. **ElevatorSimulator** created with these values
4. **run()** loops through `[2, 9, 1, 32]`:
   - Floor 2: `visit_floor(2)` → travel (100s) → open (2s) → transfer (4s) → close (2s)
   - Floor 9: `visit_floor(9)` → travel (70s) → open (2s) → transfer (4s) → close (2s)
   - Floor 1: `visit_floor(1)` → travel (80s) → open (2s) → transfer (4s) → close (2s)
   - Floor 32: `visit_floor(32)` → travel (310s) → open (2s) → transfer (4s) → close (2s)
5. **Total time**: 592 seconds
6. **Output**: `"OUTPUT: 592 12,2,9,1,32"`

---

## Key Implementation Details

### Time Calculation
- Travel: `abs(target - current) * 10`
- Each stop: 2s (open) + 4s (transfer) + 2s (close) = 8s overhead
- Total = sum of all travel times + (8s × number of stops)

### Status Messages
- Printed during each operation for real-time feedback
- Small 0.1s delay between messages for readability (only in real-time mode)

### Edge Case Handling
- If elevator is already at requested floor: skip travel, just do door operations and transfer
- Prevents unnecessary travel time calculation

### List Building
- `visited_floors` starts with starting floor
- Each floor is appended as it's visited
- Final list represents the complete path taken

---

## Potential Extensions

The current design makes it easy to add:
- Route optimization (sort floors before visiting)
- Multiple elevators (create multiple `ElevatorSimulator` instances)
- Capacity limits (track passenger count in state)
- Priority floors (modify visit order)
- Logging to file (modify `print_status` method)
- Different timing for different operations (make constants instance variables)

---

## Summary

The code follows a clean, object-oriented design that:
- Separates concerns (parsing, simulation, output)
- Maintains clear state through instance variables
- Uses method composition to build complex operations from simple ones
- Handles errors gracefully
- Provides flexibility through flags and multiple input formats

The structure is straightforward and maintainable, making it easy to understand the flow and modify behavior as needed.


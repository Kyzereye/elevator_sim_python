# Program Flow: Elevator Simulation

This document traces the execution flow of the elevator simulation from start to finish.

---

## Entry Point

**Line 172-173:**
```python
if __name__ == "__main__":
    main()
```

**What happens:**
- Python checks if script is run directly (not imported)
- If true, calls `main()` function
- **This is where execution begins**

---

## Main Function Flow

### Step 1: Argument Validation (Lines 148-151)
```python
if len(sys.argv) < 2:
    print("Usage: ...")
    sys.exit(1)
```

**Flow:**
- Checks if user provided command-line arguments
- If no arguments → print usage message → exit with error code 1
- If arguments exist → continue

### Step 2: Parse Arguments (Lines 153-157)
```python
real_time = False
input_str = sys.argv[1]
if len(sys.argv) > 2 and "--real-time" in sys.argv:
    real_time = True
```

**Flow:**
- Sets default `real_time = False` (instant calculation, no delays)
- Gets input string from `sys.argv[1]` (first argument)
- Checks for `--real-time` flag → sets `real_time = True` if found (enables delays)

### Step 3: Input Parsing (Line 160)
```python
start_floor, floors_to_visit = parse_input(input_str)
```

**Flow:**
- Calls `parse_input()` function
- Passes input string
- Receives back: `start_floor` (int) and `floors_to_visit` (list)

**Inside `parse_input()` (Lines 112-143):**
1. Strips whitespace from input
2. Detects format (key-value or simple)
3. Extracts start floor and floors list
4. Converts strings to integers
5. Returns tuple: `(start_floor, floors_list)`
6. If invalid → raises `ValueError` (caught in main)

### Step 4: Create Simulator (Line 161)
```python
simulator = ElevatorSimulator(start_floor, floors_to_visit, real_time=real_time)
```

**Flow:**
- Creates new `ElevatorSimulator` object
- Calls `__init__()` method automatically

**Inside `__init__()` (Lines 22-30):**
1. Sets `self.current_floor = start_floor`
2. Sets `self.floors_to_visit = floors_to_visit`
3. Sets `self.real_time = real_time`
4. Initializes `self.total_time = 0`
5. Initializes `self.travel_time = 0`
6. Initializes `self.door_operation_time = 0`
7. Initializes `self.passenger_transfer_time = 0`
8. Initializes `self.visited_floors = [start_floor]`
9. Returns (object is now ready)

### Step 5: Run Simulation (Line 162)
```python
total_time, visited_floors = simulator.run()
```

**Flow:**
- Calls `run()` method on simulator object
- Receives back: `total_time` and `visited_floors` tuple

### Step 6: Print Final Output (Line 163)
```python
print(f"OUTPUT: {total_time} {','.join(map(str, visited_floors))}")
```

**Flow:**
- Formats and prints final result
- Program ends (returns to system)

### Error Handling (Lines 164-169)
- If `ValueError` raised → print error → exit with code 1
- If `KeyboardInterrupt` (Ctrl+C) → print message → exit with code 1

---

## Inside `run()` Method - The Main Loop

**Lines 90-109**

### Initial Setup (Lines 92-94)
```python
print(f"\n=== Elevator Simulation Starting ===")
print(f"Starting floor: {self.current_floor}")
print(f"Floors to visit: {', '.join(map(str, self.floors_to_visit))}\n")
```
- Prints header information
- Shows starting floor and floors to visit

### Main Loop (Lines 107-118)
```python
for floor in self.floors_to_visit:
    if floor == self.current_floor:
        # Already at this floor
        self.total_time += self.open_doors(floor)
        self.total_time += self.transfer_passengers(floor)
        self.total_time += self.close_doors(floor)
    else:
        time_elapsed, time_elapsed_doors, time_elapsed_passengers, time_elapsed_travel = self.visit_floor(floor)
        self.travel_time += time_elapsed_travel
        self.door_operation_time += time_elapsed_doors
        self.passenger_transfer_time += time_elapsed_passengers
        self.total_time += time_elapsed
```

**Flow for each floor:**
1. Check if already at floor
   - **If yes:** Skip travel, just do doors + transfer (updates `total_time` only)
   - **If no:** Call `visit_floor()` which returns 4 time values
2. Unpack the 4 time values from `visit_floor()`
3. Add each time component to its respective instance variable:
   - `travel_time` - time spent moving between floors
   - `door_operation_time` - time for opening and closing doors
   - `passenger_transfer_time` - time for passenger transfers
   - `total_time` - sum of all operations

### Final Summary (Lines 120-125)
```python
print(f"\n=== Simulation Complete ===")
print(f"Total time: {self.total_time} seconds")
print(f"Total door operation time: {self.door_operation_time} seconds")
print(f"Total passenger transfer time: {self.passenger_transfer_time} seconds")
print(f"Total travel time: {self.travel_time} seconds")
print(f"Floors visited in order: {','.join(map(str, self.visited_floors))}\n")
```
- Prints completion message
- Shows detailed time breakdown (total, doors, passengers, travel)
- Shows visited floors

### Return (Line 109)
```python
return self.total_time, self.visited_floors
```
- Returns tuple to `main()` function

---

## Inside `visit_floor()` Method - Floor Visit Sequence

**Lines 75-99**

Called from `run()` when elevator needs to visit a new floor. Returns 4 time values for detailed tracking.

### Step 1: Travel (Lines 83-85)
```python
time_elapsed_travel += self.travel_to_floor(target_floor)
self.current_floor = target_floor
self.visited_floors.append(target_floor)
```

**Inside `travel_to_floor()` (Lines 59-73):**
1. Calculates distance: `abs(target_floor - self.current_floor)`
2. Calculates travel time: `distance * 10`
3. Determines direction (up/down)
4. Calls `self.print_status()` with travel message
5. If real-time: `time.sleep(travel_time)`
6. Returns travel time

**Inside `print_status()` (Lines 32-36):**
- Prints the message
- If real-time: `time.sleep(0.1)` for readability

**Time tracking:**
- Travel time is stored in `time_elapsed_travel` (separate from other times)

### Step 2: Open Doors (Line 88)
```python
time_elapsed_doors += self.open_doors(target_floor)
```

**Inside `open_doors()` (Lines 38-43):**
1. Calls `self.print_status()` with "doors opening" message
2. If real-time: `time.sleep(DOOR_OPEN_TIME)` (2 seconds)
3. Returns `DOOR_OPEN_TIME` (2)

**Time tracking:**
- Door time is added to `time_elapsed_doors` (will also include close time)

### Step 3: Transfer Passengers (Line 91)
```python
time_elapsed_passengers += self.transfer_passengers(target_floor)
```

**Inside `transfer_passengers()` (Lines 52-57):**
1. Calls `self.print_status()` with "passenger transfer" message
2. If real-time: `time.sleep(PASSENGER_TRANSFER_TIME)` (4 seconds)
3. Returns `PASSENGER_TRANSFER_TIME` (4)

**Time tracking:**
- Passenger time is stored in `time_elapsed_passengers`

### Step 4: Close Doors (Line 94)
```python
time_elapsed_doors += self.close_doors(target_floor)
```

**Inside `close_doors()` (Lines 45-50):**
1. Calls `self.print_status()` with "doors closing" message
2. If real-time: `time.sleep(DOOR_CLOSE_TIME)` (2 seconds)
3. Returns `DOOR_CLOSE_TIME` (2)

**Time tracking:**
- Close time is added to `time_elapsed_doors` (combined with open time)

### Step 5: Calculate Total (Line 97)
```python
time_elapsed = time_elapsed_doors + time_elapsed_passengers + time_elapsed_travel
```
- Sums all time components to get total time for this floor visit

### Return (Line 99)
```python
return time_elapsed, time_elapsed_doors, time_elapsed_passengers, time_elapsed_travel
```
- Returns tuple of 4 values: (total, doors, passengers, travel)
- Allows `run()` to track times separately
- Gets unpacked in `run()` and added to respective instance variables

---

## Complete Call Chain Diagram

```
Program Start
    │
    ├─> if __name__ == "__main__"
    │       │
    │       └─> main()
    │           │
    │           ├─> Check arguments (sys.argv)
    │           │
    │           ├─> parse_input(input_str)
    │           │   │
    │           │   ├─> Detect format
    │           │   ├─> Extract values
    │           │   └─> Return (start_floor, floors_list)
    │           │
    │           ├─> ElevatorSimulator.__init__()
    │           │   │
    │           │   └─> Initialize state variables
    │           │
    │           ├─> simulator.run()
    │           │   │
    │           │   ├─> Print header
    │           │   │
    │           │   ├─> for each floor in floors_to_visit:
    │           │   │   │
    │           │   │   ├─> if already at floor:
    │           │   │   │   │
    │           │   │   │   ├─> open_doors()
    │           │   │   │   │   └─> print_status()
    │           │   │   │   │
    │           │   │   │   ├─> transfer_passengers()
    │           │   │   │   │   └─> print_status()
    │           │   │   │   │
    │           │   │   │   └─> close_doors()
    │           │   │   │       └─> print_status()
    │           │   │   │
    │           │   │   └─> else:
    │           │   │       │
    │           │   │       └─> visit_floor()
    │           │   │           │
    │           │   │           ├─> travel_to_floor()
    │           │   │           │   └─> print_status()
    │           │   │           │
    │           │   │           ├─> open_doors()
    │           │   │           │   └─> print_status()
    │           │   │           │
    │           │   │           ├─> transfer_passengers()
    │           │   │           │   └─> print_status()
    │           │   │           │
    │           │   │           └─> close_doors()
    │           │   │               └─> print_status()
    │           │   │
    │           │   └─> Print summary
    │           │   └─> Return (total_time, visited_floors)
    │           │
    │           └─> Print final OUTPUT
    │
    └─> Program End
```

---

## Execution Flow Example

**Input:** `"start=12 floor=2,9,1,32"`

### Step-by-Step Execution:

1. **Entry Point**
   - `if __name__ == "__main__"` → True
   - Calls `main()`

2. **main() starts**
   - Checks `sys.argv` → has arguments, continue
   - Sets `real_time = True`
   - Gets `input_str = "start=12 floor=2,9,1,32"`

3. **parse_input() called**
   - Detects key-value format
   - Extracts: `start_floor = 12`, `floors = [2, 9, 1, 32]`
   - Returns `(12, [2, 9, 1, 32])`

4. **ElevatorSimulator created**
   - `__init__()` sets: `current_floor=12`, `floors_to_visit=[2,9,1,32]`, etc.

5. **simulator.run() called**
   - Prints header
   - Starts loop: `for floor in [2, 9, 1, 32]:`

6. **First iteration: floor = 2**
   - Not at floor 2 → calls `visit_floor(2)`
   - `visit_floor(2)`:
     - `travel_to_floor(2)` → travels 10 floors down (100s)
     - `open_doors(2)` → 2s
     - `transfer_passengers(2)` → 4s
     - `close_doors(2)` → 2s
     - Returns 108s
   - `total_time` now = 108

7. **Second iteration: floor = 9**
   - Not at floor 9 → calls `visit_floor(9)`
   - `visit_floor(9)`:
     - `travel_to_floor(9)` → travels 7 floors up (70s)
     - `open_doors(9)` → 2s
     - `transfer_passengers(9)` → 4s
     - `close_doors(9)` → 2s
     - Returns 78s
   - `total_time` now = 186

8. **Third iteration: floor = 1**
   - Not at floor 1 → calls `visit_floor(1)`
   - `visit_floor(1)`:
     - `travel_to_floor(1)` → travels 8 floors down (80s)
     - `open_doors(1)` → 2s
     - `transfer_passengers(1)` → 4s
     - `close_doors(1)` → 2s
     - Returns 88s
   - `total_time` now = 274

9. **Fourth iteration: floor = 32**
   - Not at floor 32 → calls `visit_floor(32)`
   - `visit_floor(32)`:
     - `travel_to_floor(32)` → travels 31 floors up (310s)
     - `open_doors(32)` → 2s
     - `transfer_passengers(32)` → 4s
     - `close_doors(32)` → 2s
     - Returns 318s
   - `total_time` now = 592

10. **Loop ends**
    - Prints summary
    - Returns `(592, [12, 2, 9, 1, 32])`

11. **main() continues**
    - Prints: `"OUTPUT: 592 12,2,9,1,32"`

12. **Program ends**
    - Returns to system

---

## Key Flow Points

### Where It Starts
- **Line 173:** `main()` is called when script is executed

### Main Execution Path
1. `main()` → validates arguments
2. `main()` → calls `parse_input()` → gets structured data
3. `main()` → creates `ElevatorSimulator` object
4. `main()` → calls `simulator.run()`
5. `run()` → loops through floors
6. `run()` → calls `visit_floor()` for each floor
7. `visit_floor()` → calls `travel_to_floor()`, `open_doors()`, `transfer_passengers()`, `close_doors()`
8. Each operation → calls `print_status()` for output
9. `run()` → returns results to `main()`
10. `main()` → prints final output

### Where It Ends
- **Line 163:** After printing final OUTPUT, `main()` completes
- Program returns to system (exit code 0 = success)

### Error Paths
- Invalid arguments → print usage → `sys.exit(1)`
- Invalid input → `ValueError` → print error → `sys.exit(1)`
- Ctrl+C → `KeyboardInterrupt` → print message → `sys.exit(1)`

---

## Method Call Hierarchy

```
main()
├── parse_input()
│
├── ElevatorSimulator.__init__()
│
└── simulator.run()
    ├── print_status() [multiple times]
    │
    └── for each floor:
        ├── visit_floor()
        │   ├── travel_to_floor()
        │   │   └── print_status()
        │   │
        │   ├── open_doors()
        │   │   └── print_status()
        │   │
        │   ├── transfer_passengers()
        │   │   └── print_status()
        │   │
        │   └── close_doors()
        │       └── print_status()
        │
        └── OR (if already at floor):
            ├── open_doors()
            ├── transfer_passengers()
            └── close_doors()
```

---

## Summary

**Start:** `if __name__ == "__main__"` → `main()`

**Flow:** 
1. Parse input
2. Create simulator
3. Run simulation (loop through floors)
4. For each floor: travel → open → transfer → close
5. Accumulate time and track visited floors

**End:** Print final output → return to system

The program follows a linear flow with a main loop that processes each floor sequentially, calling helper methods to perform each operation.


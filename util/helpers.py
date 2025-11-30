"""
Helper functions for input parsing and validation.
"""

from util.constants import MIN_FLOOR, MAX_FLOOR


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
            # floors.append(int(f_clean))
            floors = [int(f.strip()) for f in floors_str.split(",") if f.strip()]
        except ValueError:
            raise ValueError(f"All floors must be numbers. Got: '{f_clean}'")
    
    if not floors:
        raise ValueError("At least one floor must be specified in the floor list.")
    
    return start_floor, floors

# floors = [int(f.strip()) for f in floors_str.split(",") if f.strip()]
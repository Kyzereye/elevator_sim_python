#!/usr/bin/env python3
"""
Test suite for elevator simulation.
Uses Python's unittest module (standard library).
"""

import unittest
from classes import Timer, Elevator, StandardElevator, FastElevator
from util import validate_floor, parse_input
from util.constants import MIN_FLOOR, MAX_FLOOR


class TestTimer(unittest.TestCase):
    """Test cases for Timer class."""
    
    def test_calculate_travel_time_static(self):
        """Test static method calculate_travel_time."""
        # Test with class call
        result = Timer.calculate_travel_time(5, 10)
        self.assertEqual(result, 50)
        
        # Test with instance call
        timer = Timer()
        result = timer.calculate_travel_time(3, 10)
        self.assertEqual(result, 30)
    
    def test_timer_initialization(self):
        """Test Timer initialization."""
        timer = Timer(real_time=False)
        self.assertFalse(timer.real_time)
        self.assertEqual(timer.total_elapsed, 0)
    
    def test_timer_sleep_no_delay(self):
        """Test timer sleep without real-time delay."""
        timer = Timer(real_time=False)
        result = timer.sleep(5.0)
        self.assertEqual(result, 5.0)
        # Should not actually sleep, so this should be fast
    
    def test_timer_reset(self):
        """Test timer reset functionality."""
        timer = Timer()
        timer.total_elapsed = 100
        timer.reset()
        self.assertEqual(timer.total_elapsed, 0)


class TestFloorValidation(unittest.TestCase):
    """Test cases for floor validation."""
    
    def test_valid_floor_min(self):
        """Test minimum valid floor."""
        # Should not raise
        validate_floor(MIN_FLOOR)
    
    def test_valid_floor_max(self):
        """Test maximum valid floor."""
        # Should not raise
        validate_floor(MAX_FLOOR)
    
    def test_valid_floor_middle(self):
        """Test middle valid floor."""
        validate_floor(15)
    
    def test_invalid_floor_too_low(self):
        """Test floor below minimum."""
        with self.assertRaises(ValueError):
            validate_floor(MIN_FLOOR - 1)
    
    def test_invalid_floor_too_high(self):
        """Test floor above maximum."""
        with self.assertRaises(ValueError):
            validate_floor(MAX_FLOOR + 1)


class TestInputParsing(unittest.TestCase):
    """Test cases for input parsing."""
    
    def test_valid_input(self):
        """Test valid input parsing."""
        start, floors = parse_input("start=12 floor=2,9,1,32")
        self.assertEqual(start, 12)
        self.assertEqual(floors, [2, 9, 1, 32])
    
    def test_input_with_whitespace(self):
        """Test input with extra whitespace."""
        start, floors = parse_input("start= 12  floor= 2 , 9 , 1 , 32 ")
        self.assertEqual(start, 12)
        self.assertEqual(floors, [2, 9, 1, 32])
    
    def test_input_single_floor(self):
        """Test input with single floor."""
        start, floors = parse_input("start=5 floor=10")
        self.assertEqual(start, 5)
        self.assertEqual(floors, [10])
    
    def test_invalid_input_missing_start(self):
        """Test input missing start parameter."""
        with self.assertRaises(ValueError):
            parse_input("floor=2,9")
    
    def test_invalid_input_missing_floor(self):
        """Test input missing floor parameter."""
        with self.assertRaises(ValueError):
            parse_input("start=12")
    
    def test_invalid_input_non_numeric_start(self):
        """Test input with non-numeric start floor."""
        with self.assertRaises(ValueError):
            parse_input("start=abc floor=2,9")
    
    def test_invalid_input_non_numeric_floor(self):
        """Test input with non-numeric floor."""
        with self.assertRaises(ValueError):
            parse_input("start=12 floor=2,abc,9")
    
    def test_invalid_input_empty_floor_list(self):
        """Test input with empty floor list."""
        with self.assertRaises(ValueError):
            parse_input("start=12 floor=")


class TestElevator(unittest.TestCase):
    """Test cases for Elevator base class."""
    
    def test_elevator_initialization(self):
        """Test elevator initialization."""
        elevator = Elevator(start_floor=5, floors_to_visit=[10, 15])
        self.assertEqual(elevator.current_floor, 5)
        self.assertEqual(elevator.floors_to_visit, [10, 15])
        self.assertFalse(elevator.real_time)
        self.assertEqual(elevator.total_time, 0)
        self.assertEqual(elevator.visited_floors, [5])
    
    def test_current_floor_property_setter(self):
        """Test current_floor property setter with validation."""
        elevator = Elevator(start_floor=5, floors_to_visit=[])
        
        # Valid floor
        elevator.current_floor = 10
        self.assertEqual(elevator.current_floor, 10)
        
        # Invalid floor - too high
        with self.assertRaises(ValueError):
            elevator.current_floor = MAX_FLOOR + 1
        
        # Invalid floor - too low
        with self.assertRaises(ValueError):
            elevator.current_floor = MIN_FLOOR - 1
    
    def test_current_floor_type_validation(self):
        """Test current_floor property type validation."""
        elevator = Elevator(start_floor=5, floors_to_visit=[])
        
        # Non-integer should raise TypeError
        with self.assertRaises(TypeError):
            elevator.current_floor = 5.5
    
    def test_timer_composition(self):
        """Test that elevator has a Timer (composition)."""
        elevator = Elevator(start_floor=5, floors_to_visit=[])
        self.assertIsInstance(elevator.timer, Timer)
    
    def test_travel_to_floor_same_floor(self):
        """Test traveling to the same floor (should be 0 time)."""
        elevator = Elevator(start_floor=5, floors_to_visit=[])
        travel_time = elevator.travel_to_floor(5)
        self.assertEqual(travel_time, 0)
        self.assertEqual(elevator.current_floor, 5)
    
    def test_travel_to_floor_up(self):
        """Test traveling up floors."""
        elevator = Elevator(start_floor=5, floors_to_visit=[])
        travel_time = elevator.travel_to_floor(10)
        # 5 floors * 10 seconds = 50 seconds
        self.assertEqual(travel_time, 50)
        # Note: current_floor is updated in visit_floor(), not travel_to_floor()
        # So it should still be 5 here
    
    def test_travel_to_floor_down(self):
        """Test traveling down floors."""
        elevator = Elevator(start_floor=10, floors_to_visit=[])
        travel_time = elevator.travel_to_floor(5)
        # 5 floors * 10 seconds = 50 seconds
        self.assertEqual(travel_time, 50)
        # Note: current_floor is updated in visit_floor(), not travel_to_floor()
        # So it should still be 10 here
    
    def test_get_stats(self):
        """Test get_stats method."""
        elevator = Elevator(start_floor=5, floors_to_visit=[10])
        elevator.total_time = 100
        elevator.travel_time = 50
        elevator.door_operation_time = 30
        elevator.passenger_transfer_time = 20
        
        stats = elevator.get_stats()
        self.assertEqual(stats['total_time'], 100)
        self.assertEqual(stats['travel_time'], 50)
        self.assertEqual(stats['door_operation_time'], 30)
        self.assertEqual(stats['passenger_transfer_time'], 20)
        self.assertEqual(stats['visited_floors'], [5])


class TestStandardElevator(unittest.TestCase):
    """Test cases for StandardElevator."""
    
    def test_standard_elevator_inheritance(self):
        """Test that StandardElevator inherits from Elevator."""
        elevator = StandardElevator(start_floor=5, floors_to_visit=[10])
        self.assertIsInstance(elevator, Elevator)
        self.assertEqual(elevator.FLOOR_TRAVEL_TIME, 10)
    
    def test_standard_elevator_timing(self):
        """Test standard elevator timing."""
        elevator = StandardElevator(start_floor=5, floors_to_visit=[])
        travel_time = elevator.travel_to_floor(10)
        # 5 floors * 10 seconds = 50 seconds
        self.assertEqual(travel_time, 50)


class TestFastElevator(unittest.TestCase):
    """Test cases for FastElevator."""
    
    def test_fast_elevator_inheritance(self):
        """Test that FastElevator inherits from Elevator."""
        elevator = FastElevator(start_floor=5, floors_to_visit=[10])
        self.assertIsInstance(elevator, Elevator)
        self.assertEqual(elevator.FLOOR_TRAVEL_TIME, 5)
    
    def test_fast_elevator_timing(self):
        """Test fast elevator timing (twice as fast)."""
        elevator = FastElevator(start_floor=5, floors_to_visit=[])
        travel_time = elevator.travel_to_floor(10)
        # 5 floors * 5 seconds = 25 seconds (half of standard)
        self.assertEqual(travel_time, 25)
    
    def test_fast_elevator_polymorphism(self):
        """Test that FastElevator overrides FLOOR_TRAVEL_TIME."""
        standard = StandardElevator(start_floor=5, floors_to_visit=[])
        fast = FastElevator(start_floor=5, floors_to_visit=[])
        
        self.assertEqual(standard.FLOOR_TRAVEL_TIME, 10)
        self.assertEqual(fast.FLOOR_TRAVEL_TIME, 5)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete simulation flow."""
    
    def test_simple_simulation(self):
        """Test a simple simulation run."""
        elevator = StandardElevator(start_floor=1, floors_to_visit=[2, 3])
        total_time, visited_floors = elevator.run()
        
        # Should visit floors 1, 2, 3
        self.assertEqual(visited_floors, [1, 2, 3])
        # Total time should be positive
        self.assertGreater(total_time, 0)
    
    def test_already_at_floor(self):
        """Test simulation when starting floor is in visit list."""
        elevator = StandardElevator(start_floor=5, floors_to_visit=[5, 10])
        total_time, visited_floors = elevator.run()
        
        # Floor 5 is already in visited_floors from initialization
        # When already at floor, it performs operations but doesn't add duplicate
        # So visited_floors should be [5, 10] (5 from init, 10 from visit)
        self.assertEqual(visited_floors, [5, 10])
        self.assertGreater(total_time, 0)


if __name__ == '__main__':
    unittest.main()


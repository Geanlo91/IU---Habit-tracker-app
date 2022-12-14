import pytest
from db import *
from tracker import *

def db_connection():
    db = sqlite3.connect("habits.db")
    return db

# Test for creating a habit
def test_track_habit():
    habit = track_habit("Habit 1", "2021-01-01", "2021-01-01", "Daily", 1,0,0,0,"No")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "No"

# Test for editing a habit
def test_edit_habit():
    habit = edit_habit("Habit 1", "2021-01-01", "2021-01-01", "Daily", 1)
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1

# Test for deleting a habit
def test_delete_habit():
    habit = delete_habit("Habit 1")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "No"

# Test for completing a habit
def test_complete_habit():
    habit = complete_habit("Habit 1", "Yes")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "Yes"

# Test for resetting a habit
def test_reset_habit():
    habit = reset_habit("Habit 1", 0,0,0,"No")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "No"

# Test for getting all habits
def test_get_all_habits():
    habit = get_habits()
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "No"

# Test for getting a habit
def test_get_habit():
    habit = get_habit("Habit 1")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "No"

# Test for getting a habit by name
def test_get_habit_by_name():
    habit = get_habit("Habit 1")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2021-01-01"
    assert habit.start_date == "2021-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 1
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.success_rate == 0
    assert habit.completed == "No"



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
    if habit_exist_check("Habit 1") == True:
        habit = edit_habit("Habit 1", "2021-01-01", "2021-01-01", "Daily", 1)
        assert habit.Habit_name == "Habit 1"
        assert habit.created == "2021-01-01"
        assert habit.start_date == "2021-01-01"
        assert habit.Periodicity == "Daily"
        assert habit.Run_duration == 1
    else:
        print("Habit does not exist")
        

# Test for deleting a habit
def test_delete_habit():
    if habit_exist_check("Habit 1") == True:
        habit = delete_habit()
        assert habit.Habit_name == "Habit 1"
    else:
        print("Habit does not exist")

# Test for completing a habit
def test_complete_habit():
    if habit_exist_check("Habit 1") == True and complete_habit("Habit 1") == False:
        habit = complete_habit("Habit 1", "Yes")
        assert habit.Habit_name == "Habit 1"
        assert habit.completed == "Yes"
    else:
        print("Habit does not exist")

# Test for resetting a habit
def test_reset_habit():
    if habit_exist_check("Habit 1") == True:
        habit = reset_habit("Habit 1","2021-01-01", 0,0,0,"No")
        assert habit.Habit_name == "Habit 1"
        assert habit.created == "2021-01-01"
        assert habit.start_date == "2021-01-01"
        assert habit.Periodicity == "Daily"
        assert habit.Run_duration == 1
        assert habit.streak == 0
        assert habit.longest_streak == 0
        assert habit.success_rate == 0
        assert habit.completed == "No"
    else:
        print("Habit does not exist")



# Test for getting all habits
def test_get_all_habits():
    if habit_exist_check("Habit 1") == True:
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
    if habit_exist_check("Habit 1") == True:
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
    else:
        print("Habit does not exist")

# Test checking off a habit
def test_check_off_habit():
    if habit_exist_check("Habit 1") == True:
        habit = check_off_habit("Habit 1", "No")
        assert habit.Habit_name == "Habit 1"
        assert habit.completed == "No"
    else:
        print("Habit does not exist")


def test_add_habit():
    if habit_exist_check("Habit 1") == False:
        habit = add_habit("Habit 1", "2021-01-01", "2021-01-01", "Daily", 1,"No")
        assert habit.Habit_name == "Habit 1"
        assert habit.created == "2021-01-01"
        assert habit.start_date == "2021-01-01"
        assert habit.Periodicity == "Daily"
        assert habit.Run_duration == 1
        assert habit.completed == "No"
    else:
        print("Habit already exists")



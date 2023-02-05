import pytest
from db import *
from tracker import *
conn = sqlite3.connect("main.db")
from db import prehabits
from testdb import *
from tabulate import tabulate



def db_connection():
    '''
    This function creates a connection to the database and tests if the connection is successful.
    '''
    db = sqlite3.connect("habits.db")
    return db

# Test for creating a habit
def test_track_habit():
    habit = track_habit("Habit 1", "2023-01-01", "2023-01-01", "Daily", 10, "2023-01-03", 0, 0, "No")
    assert habit.Habit_name == "Habit 1"
    assert habit.created == "2023-01-01"
    assert habit.start_date == "2023-01-01"
    assert habit.Periodicity == "Daily"
    assert habit.Run_duration == 10
    assert habit.Checked == "2023-01-03"
    assert habit.streak == 0
    assert habit.longest_streak == 0
    assert habit.completed == "No"

# Test for editing a habit
def test_edit_habit():
    if habit_exist_check("Habit 1") == True:
        habit = edit_habit("Habit 1")
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
        habit = delete_habit("Habit 1")
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
        habit = reset_habit("Habit 1")
        assert habit.Habit_name == "Habit 1"
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
        assert habit.Checked == "2021-01-01"
        assert habit.streak == 0
        assert habit.longest_streak == 0
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
        assert habit.Checked == "2021-01-01"
        assert habit.streak == 0
        assert habit.longest_streak == 0
        assert habit.completed == "No"
    else:
        print("Habit does not exist")

# Test checking off a habit
def test_check_off_habit():
    if habit_exist_check("Habit 1") == True:
        habit = check_off_habit("Habit 1", "Daily","2023-01-20")
        assert habit.Habit_name == "Habit 1"
        assert habit.Periodicity == "Daily"
        assert habit.Checked == "2023-01-20"
    else:
        print("Habit does not exist")



'''Below we are Running tests on the habits saved in the prehabits table and the testdb'''

def test_add_habit2():
    testdb = get_test_db()
    curs = testdb.cursor()
    #inserting a habit into the prehabits2 table
    curs.execute("Insert into prehabits2 (Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) values ('Habit 1', '2021-01-01', '2021-01-01', 'Daily', 1, '2021-01-01', 0, 0, 'No')")
    testdb.commit()
    #Retrieving the habit from the prehabits2 table
    curs.execute("Select * from prehabits2 where Habit_name = 'Habit 1'")
    habit = curs.fetchone()
    #delete the habit from the prehabits2 table
    curs.execute("Delete from prehabits2 where Habit_name = 'Habit 1'")
    testdb.commit()


# Test for getting a habit from the prehabits2 table
def test_get_habit2():
    testdb = get_test_db()
    curs = testdb.cursor()
    #inserting a habit into the prehabits2 table
    curs.execute("INSERT into prehabits2 (Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) values ('Habit 1', '2021-01-01', '2021-01-01', 'Daily', 1, '2021-01-01', 0, 0, 'No')")
    testdb.commit()
    #Retrieving the habit from the prehabits2 table
    habit = get_habit2("Habit 1")
    assert habit[0] == "Habit 1"
    assert habit[1] == "2021-01-01"
    assert habit[2] == "2021-01-01"
    assert habit[3] == "Daily"
    assert habit[4] == 1
    assert habit[5] == "2021-01-01"
    assert habit[6] == 0
    assert habit[7] == 0
    assert habit[8] == "No"
    #printing the test database
    curs.execute("Select * from prehabits2")
    print(curs.fetchall())
    #delete the habit from the prehabits table
    curs.execute("Delete from prehabits2 where Habit_name = 'Habit 1'")
    testdb.commit()

#testing streak and longest streak calculations
def test_streak_calculation():
    '''checking if any changes to the checked date will change the streak and longest streak'''
    testdb = get_test_db()
    curs = testdb.cursor()
    #inserting a habit into the prehabits2 table
    curs.execute("INSERT into prehabits2 (Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) values ('Habit 1', '2021-01-01', '2021-01-01', 'Daily', 10, '2021-01-01', 0, 0, 'No')")
    testdb.commit()
    #Retrieving the habit from the prehabits2 table
    habit = get_habit2("Habit 1")
    print(habit)
    #testing the streak calculation
    streak = streak_calculation("Habit 1", "2021-01-03")
    assert habit.streak == 1
    #testing the longest streak calculation
    longest_streak = longest_streak_calculation("Habit 1", "2021-01-03")
    assert habit.longest_streak == 1
    #delete the habit from the prehabits2 table
    curs.execute("Delete from prehabits2 where Habit_name = 'Habit 1'")
    testdb.commit()


#testing reseting habits stored in the prehabits2 database
def test_reset_habit2():
    '''The logic is to change streak and longest streak to 0 and change the checked date to the current date'''
    testdb = get_test_db()
    curs = testdb.cursor()
    #inserting a habit into the prehabits2 table
    curs.execute("INSERT into prehabits2 (Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) values ('Habit 1', '2021-01-01', '2021-01-01', 'Daily', 1, '2021-01-01', 0, 0, 'No')")
    testdb.commit()
    #Retrieving the habit from the prehabits2 table
    habit = get_habit2("Habit 1")
    #testing the reset habit function
    reset_habit2("Habit 1")
    #printing the test database
    curs.execute("Select * from prehabits2")
    print(curs.fetchall())
    #delete the habit from the prehabits table
    curs.execute("Delete from prehabits2 where Habit_name = 'Habit 1'")


#testing getting all habits from the prehabits2 database
def test_get_all_habits2():
    '''The idea is to check if the function returns all the habits in the prehabits2 database'''
    testdb = get_test_db()
    curs = testdb.cursor()
    #retrieve all habits from the prehabits2 table
    habits = get_habits2()
    #printing the test database
    print(habits)
    
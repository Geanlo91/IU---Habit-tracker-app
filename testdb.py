import sqlite3 
from datetime import date, datetime
from tabulate import tabulate
conn = sqlite3.connect("main.db")
import pandas as pd
from datetime import timedelta
con = sqlite3.connect("test.db")
from tabulate import tabulate
from collections import namedtuple




def get_test_db(name="test.db"):

    '''
    Defining the database and its name (test.db)
    '''
    testdb = sqlite3.connect(name)
    create_tables(testdb) 
    return testdb


def create_tables(testdb):
    '''
    Creating the habit table in the database that will house all created habits.
    '''
    curs = testdb.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS prehabits2(
        Habit_name TEXT,
        created TEXT,
        start_date TEXT,
        Periodicity TEXT,
        Run_duration INTEGER,
        Checked DATE, 
        streak INTEGER, 
        longest_streak INTEGER, 
        completed TEXT
    )""")

    curs.execute("""INSERT INTO prehabits2(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES(?,?,?,?,?,?,?,?,?)""", 
          ('Jogging', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'))
    curs.execute("""INSERT INTO prehabits2(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES(?,?,?,?,?,?,?,?,?)""",
          ('Studying', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'))
    curs.execute("""INSERT INTO prehabits2(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES(?,?,?,?,?,?,?,?,?)""",
          ('Meditating', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'))
    curs.execute("""INSERT INTO prehabits2(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES(?,?,?,?,?,?,?,?,?)""",
          ('Blogging', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'))
    curs.execute("""INSERT INTO prehabits2(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES(?,?,?,?,?,?,?,?,?)""",
          ('Art', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'))
    curs.execute("""INSERT INTO prehabits2(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES(?,?,?,?,?,?,?,?,?)""",
          ('Code', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'))      
    testdb.commit()
    return testdb


def add_habit2(habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed):
    '''
    Adding a habit to the database
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("INSERT INTO prehabits2 (Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed))
    testdb.commit()
    print(tabulate(curs.fetchall(), headers=["Habit_name", "created", "start_date", "Periodicity", "Run_duration", "Checked", "streak", "longest_streak", "completed"]))
    return testdb


def get_habits2():
    '''
    Getting all habits from the database
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT * FROM prehabits2")
    return curs.fetchall()

Habit = namedtuple("Habit", ["Habit_name", "created", "start_date", "Periodicity", "Run_duration", "Checked", "streak", "longest_streak", "completed"])
def get_habit2(habit_name):
    '''
    Getting a specific habit from the database
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT * FROM prehabits2 WHERE habit_name = ?", (habit_name,))
    habit_tuple = curs.fetchone()
    habit = Habit(*habit_tuple)
    return habit


def update_habit2(habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed):
    '''
    Updating a specific habit from the database
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("UPDATE prehabits2 SET created = ?, start_date = ?, Periodicity = ?, Run_duration = ?, Checked = ?, streak = ?, longest_streak = ?, completed = ? WHERE Habit_name = ?", (created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed, habit_name))
    testdb.commit()
    return testdb


def delete_habit2(habit_name):
    '''
    Deleting a specific habit from the database
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("DELETE FROM prehabits2 WHERE Habit_name = ?", (habit_name,))
    testdb.commit()
    return testdb


def edit_habit2(Habit_name):
    '''
    Editing a habit's start date, periodicity and run duration. This is only possible if the habit is still active and not completed. 
    User input the Periodicity and Run_duration. 
    The start date is automatically set to the current date. The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    from datetime import datetime
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        start_date = str(datetime.now().strftime("%Y-%m-%d"))
        allowed_periodicity = ["Daily", "Weekly"]
        Periodicity = input("Enter the new periodicity (Daily, Weekly):")
        while Periodicity not in allowed_periodicity:
            print("Invalid periodicity")
            Periodicity = input("Enter the new periodicity (Daily, Weekly):")
        Run_duration = input("Enter the new duration of the habit in days:")
        curs.execute("UPDATE prehabits2 SET start_date=?, Periodicity=?, Run_duration=? WHERE Habit_name=?",
    (start_date, Periodicity, Run_duration, Habit_name))
        testdb.commit()

def complete_habit2(Habit_name):
    '''
    Completing a habit. This is only possible if the habit is still active and not completed. 
    The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        curs.execute("UPDATE prehabits2 SET completed=? WHERE Habit_name=?", ("Yes", Habit_name))
        testdb.commit()

#def streak_calculation(Habit_name,Checked):
    '''
    Calculating the streak of a habit. This is only possible if the habit is still active and not completed. 
    The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        curs.execute("SELECT Checked FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        Checked = result[0]
        curs.execute("SELECT streak FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        streak = result[0]
        curs.execute("SELECT longest_streak FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        longest_streak = result[0]
        #checking to see the difference between the checked date and current date to calculate the streak
        if date.fromisoformat(Checked) + timedelta(days=1) == date.today():
            curs.execute("UPDATE prehabits2 SET streak=? WHERE Habit_name=?", (streak + 1, Habit_name))
            testdb.commit()
        else:
            curs.execute("UPDATE prehabits2 SET streak=? WHERE Habit_name=?", (1, Habit_name))
          #checking to see if the streak is the longest streak
        if streak + 1 > longest_streak:
            curs.execute("UPDATE prehabits2 SET longest_streak=? WHERE Habit_name=?", (streak + 1, Habit_name))
            testdb.commit()
        else:
            curs.execute("UPDATE prehabits2 SET longest_streak=? WHERE Habit_name=?", (longest_streak, Habit_name))
            testdb.commit()

            
          
          

#def longest_streak_calculation(Habit_name,Checked):
    '''
    Calculating the longest streak of a habit. This is only possible if the habit is still active and not completed. 
    The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        curs.execute("SELECT streak FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        streak = result[0]
        curs.execute("SELECT longest_streak FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        longest_streak = result[0]
        if streak > longest_streak:
            longest_streak = streak
        curs.execute("UPDATE prehabits2 SET longest_streak=? WHERE Habit_name=?",
    (longest_streak, Habit_name))
        testdb.commit()
        

def reset_habit2(Habit_name):
    '''
    Resetting a habit. This is only possible if the habit is still active and not completed. 
    The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        curs.execute("UPDATE prehabits2 SET streak=?, longest_streak=? WHERE Habit_name=?",
    (0, 0, Habit_name))
        testdb.commit()


def streak_calculation(Habit_name,Checked):
    '''
    Calculating the streak of a habit. This is only possible if the habit is still active and not completed. 
    The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        if date.fromisoformat(Checked) + timedelta(days=1) == date.fromisoformat(Checked):
            curs.execute("UPDATE prehabits2 SET streak= streak + 1 WHERE Habit_name=?", (Habit_name,))
            testdb.commit()
            Checked = date.today()
        elif date.fromisoformat(Checked) + timedelta(days=1) > date.today():
            Checked = date.today()
        else:
            curs.execute("UPDATE prehabits2 SET streak= 1 WHERE Habit_name=?", (Habit_name,))
            testdb.commit()
            Checked = date.today()

        curs.execute("SELECT * FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        if result[6] >= result[7]:
            curs.execute("UPDATE prehabits2 SET Longest_streak= streak WHERE Habit_name=?", (Habit_name,))
            testdb.commit()
        if result[6] >= int(result[4]):
            curs.execute("UPDATE prehabits2 SET completed=? WHERE Habit_name=?", ("Yes", Habit_name))
            testdb.commit()


def longest_streak_calculation(Habit_name,Checked):
    '''
    Calculating the longest streak of a habit. This is only possible if the habit is still active and not completed. 
    The table is updated.
    '''
    testdb = get_test_db()
    curs = testdb.cursor()
    curs.execute("SELECT completed FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
    result = curs.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        if date.fromisoformat(Checked) + timedelta(days=7) == date.fromisoformat(Checked):
            curs.execute("UPDATE prehabits2 SET streak= streak + 1 WHERE Habit_name=?", (Habit_name,))
            testdb.commit()
            Checked = date.today()
        elif date.fromisoformat(Checked) + timedelta(days=7) > date.today():
            Checked = date.today()
        else:
            curs.execute("UPDATE prehabits2 SET streak= 1 WHERE Habit_name=?", (Habit_name,))
            testdb.commit()
            Checked = date.today()

        curs.execute("SELECT * FROM prehabits2 WHERE Habit_name=?", (Habit_name,))
        result = curs.fetchone()
        if result[6] >= result[7]:
            curs.execute("UPDATE prehabits2 SET Longest_streak= streak WHERE Habit_name=?", (Habit_name,))
            testdb.commit()
        if result[6] >= int(result[4]):
            curs.execute("UPDATE prehabits2 SET completed=? WHERE Habit_name=?", ("Yes", Habit_name))
            testdb.commit()
   
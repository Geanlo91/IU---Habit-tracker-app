import sqlite3 
from datetime import date, datetime
from tabulate import tabulate
conn = sqlite3.connect("main.db")
import pandas as pd
from calendar import calendar
from datetime import timedelta


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db) 
    return db


def create_tables(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habits(
        Habit_name TEXT PRIMARY KEY,
        created TEXT,
        start_date TEXT,
        Periodicity TEXT,
        Run_duration INTEGER,
        Checked TEXT, 
        streak INTEGER, 
        longest_streak INTEGER, 
        completed TEXT
    )""")
    db.commit()
    

    
    cur.execute("""CREATE TABLE IF NOT EXISTS habit_log( Habit_name TEXT, Checked TEXT, streak INTEGER, longest_streak INTEGER, completed TEXT,
    FOREIGN KEY(Habit_name) REFERENCES habits(Habit_name))""")
    db.commit()
    return db



def add_habit(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
    if result: 
        print()
    else:
        cur.execute("INSERT INTO habits VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed))
        db.commit()
        print("Habit added successfully") 
 


def edit_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    from datetime import datetime
    Habit_name = Habit_name
    start_date = str(datetime.now().strftime("%Y-%m-%d"))
    allowed_periodicity = ["Daily", "Weekly"]
    Periodicity = input("Enter the new periodicity (Daily, Weekly):")
    while Periodicity not in allowed_periodicity:
        print("Invalid periodicity")
        Periodicity = input("Enter the new periodicity (Daily, Weekly):")
    Run_duration = input("Enter the new duration of the habit in days:")
    cur.execute("UPDATE habits SET start_date=?, Periodicity=?, Run_duration=? WHERE Habit_name=?",
    (start_date, Periodicity, Run_duration, Habit_name))
    db.commit()

def delete_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE Habit_name=?", (Habit_name,))
    db.commit()

def complete_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    completed = "Yes"
    cur.execute("SELECT completed FROM habits Where Habit_name=?",(Habit_name,))
    result = cur.fetchone()
    if result is not None and result[0] == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        cur.execute("UPDATE habits SET completed=? WHERE Habit_name=?",
        (completed, Habit_name))
        db.commit()


def reset_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    from datetime import date
    Habit_name = Habit_name
    streak = 0
    longest_streak = 0
    completed = "No"
    cur.execute("UPDATE habits SET streak = ?, longest_streak = ?, completed = ? WHERE Habit_name=?",
    (streak, longest_streak, completed, Habit_name))
    db.commit()
    

def change_start_date(Habit_name, start_date):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET start_date=? WHERE Habit_name=?",
    (start_date, Habit_name))
    db.commit()
    

def check_off_habit(Habit_name, Periodicity, Checked):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
    if result is None:
        raise ValueError("Habit does not exist")

    previously_checked = result[5]
    current_streak = result[6]
    long_streak = int(result[7])


    if Periodicity == "Daily":
        from datetime import timedelta
        delta = timedelta(days=1)
        if previously_checked + str(timedelta(days=1)) >= Checked:
            current_streak += 1
            Checked = date.today()
        else:
            current_streak = 0
    elif Periodicity == "Weekly":
        if previously_checked + timedelta(days=7) >= Checked:
            current_streak += 1
        else:
            current_streak = 1
    else:
        raise ValueError("Invalid Periodicity:'{Periodicity}'")

    if current_streak > long_streak:
        long_streak = current_streak

    cur.execute("UPDATE habits SET streak=?, Checked=?, longest_streak=? WHERE Habit_name=?",(current_streak, Checked, long_streak, Habit_name))
    db.commit()
    

def get_habits():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    db.commit()
    return cur.fetchall()


def get_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name,))
    db.commit()
    return cur.fetchall()

def habit_exist_check(Habit_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", [Habit_name])
    habit = cur.fetchone()
    if habit:
        return True
    else:
        return False
    

    """
    Check if a habit with the given name exists in the database.
    
    Args:
        db: The database connection.
        habit_name: The name of the habit to check for.
    
    Returns:
        True if the habit exists, False otherwise.
    """
def habit_name_exist(db, Habit_name):
    db = get_db()
    cur = db.cursor()
    query = "SELECT count(*) FROM habits WHERE Habit_name=?"
    cur.execute(query, (Habit_name,))
    result = cur.fetchone()
    return result[0]>0


 


prehabits = [
    ['Running', '2021-01-01', '2021-01-01', 'Daily',45,'2021-01-02', 1, 5, 'No'],
    ['Reading', '2021-01-01', '2021-01-01', 'Weekly' ,30,'2021-01-02', 5,10, 'No'],
    ['Meditation', '2021-01-01', '2021-01-01', 'Daily', 30,'2021-01-02', 1, 5, 'No'],
    ['Playing Soccer', '2021-01-01', '2021-01-01', 'Weekly', 5,'2021-01-02', 1, 2, 'No'],
    ['Rock climbing', '2021-01-01', '2021-01-01', 'Daily',60,'2021-01-02', 1, 5, 'No']]



def delete_all_habits():
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE * FROM habits")
    db.commit()
    print (get_habits())
    
    
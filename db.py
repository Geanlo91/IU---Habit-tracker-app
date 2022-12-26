import sqlite3 
from datetime import date, datetime
from tabulate import tabulate
conn = sqlite3.connect("main.db")
import pandas as pd
from calendar import calendar


def get_db(name="main.db"):
    db = sqlite3.connect(f"{name}.db")
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
        streak INTEGER, 
        longest_streak INTEGER, 
        success_rate INTEGER, 
        completed TEXT 
    )""")
    db.commit()
    

    
    cur.execute("""CREATE TABLE IF NOT EXISTS habit_log( Habit_name TEXT, streak INTEGER, longest_streak INTEGER, success_rate INTEGER, completed TEXT,
    FOREIGN KEY(Habit_name) REFERENCES habits(Habit_name))""")
    db.commit()
    return db



def add_habit (Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name = ?", (Habit_name,))
    if cur.fetchone() is not None:
        return "Habit already exists"
    cur.execute("INSERT INTO habits (Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed))
    db.commit()
    return "Habit added successfully"


def edit_habit(start_date, Periodicity, Run_duration):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET start_date=?, Periodicity=?, Run_duration=? WHERE Habit_name=?",
    (start_date, Periodicity, Run_duration))
    db.commit()

def delete_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE Habit_name=?", (Habit_name))
    db.commit()

def complete_habit(Habit_name, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET completed=? WHERE Habit_name=?",(Habit_name, completed))
    db.commit()


def reset_habit(Habit_name, created, start_date, Periodicity, Run_duration , streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    from datetime import datetime
    cur.execute("UPDATE habits SET created = ?, start_date = ?, Run_duration = 0, streak = 0, longest_streak = 0, success_rate = 0, completed = 'No' WHERE Habit_name=?",
    (Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed))
    db.commit()
    

def change_start_date(Habit_name, start_date):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET start_date=? WHERE Habit_name=?",
    (start_date, Habit_name))
    db.commit()
    

def check_off_habit(Habit_name, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT streak FROM habits WHERE Habit_name=?", [Habit_name])
    result = cur.fetchone()
    if result is not None:
        streak = int(result[0])
    else:
        streak = 0
    cur.execute("UPDATE Habits SET streak = 'result' + 1 WHERE Habit_name=?",
    (streak,))
    db.commit()
    

def calculate_success_rate(Run_duration, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET success_rate = ((SELECT max (streak, longest_streak) FROM habits)/Run_duration) * 100")
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
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name))
    db.commit()
    return cur.fetchall()

def habit_exist_check(Habit_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name))
    habit = cur.fetchall()
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


 


prehabits = [["Habit_name", "created", "start_date", "Periodicity", "Run_duration", "streak", "longest_streak" , "success_rate" , "completed"],
    ['Running', '2021-01-01', '2021-01-01', 'Daily', 45, 1, 5, 0.2, 'No'],
    ['Reading', '2021-01-01', '2021-01-01', 'Weekly', 30, 5,10, 0.25, 'No'],
    ['Meditation', '2021-01-01', '2021-01-01', 'Daily', 30, 1, 5, 0.2, 'No'],
    ['Playing Soccer', '2021-01-01', '2021-01-01', 'Weekly', 5, 1, 2, 0.2, 'No'],
    ['Rock climbing', '2021-01-01', '2021-01-01', 'Daily', 60, 1, 5, 0.2, 'No']]

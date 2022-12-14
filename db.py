import sqlite3
from datetime import date, datetime
from tabulate import tabulate
conn = sqlite3.connect("main.db")
import pandas as pd
from calendar import calendar
import click
import pytest

def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables():
    db = get_db()
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



def add_habit(Habit_name, created, start_date, Periodicity, Run_duration, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES(?, ?, ?, ?, ?, ?)", 
    (Habit_name, created, start_date, Periodicity, Run_duration, completed))
    db.commit()


def edit_habit(Habit_name,created, start_date, Periodicity, Run_duration):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET Habit_name=?, created=?, start_date=?, Periodicity=?, Run_duration=? WHERE Habit_name=?",
    (Habit_name, created, start_date, Periodicity, Run_duration, Habit_name))
    db.commit()

def delete_habit(Habit_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE Habit_name=?", (Habit_name,))
    db.commit()

def complete_habit(Habit_name, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET completed=? WHERE Habit_name=?",
    (completed, Habit_name))
    db.commit()


def reset_habit(Habit_name, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET created = date.today(), streak = 0, longest_streak = 0, success_rate = 0, completed = 'No' WHERE Habit_name=?",
    (streak, longest_streak, success_rate, completed, Habit_name))
    db.commit()
    return cur.fetchall()

def change_start_date(Habit_name, start_date):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE habits SET start_date=? WHERE Habit_name=?",
    (start_date, Habit_name))
    db.commit()
    return cur.fetchall()

def check_off_habit(Habit_name, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT streak FROM habits WHERE completed = 'No' (UPDATE streak SET streak = streak + 1 WHERE Periodicity = 'Daily' OR Periodicity = 'Weekly'",
    (streak, longest_streak, success_rate, completed, Habit_name))
    db.commit()
    return cur.fetchall()

def calculate_success_rate(Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT success_rate FROM habits")
    success_rate = max ((streak, longest_streak)//Run_duration * 100)
    db.commit()
    return cur.fetchall()

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
    cur.execute("SELECT Habit_name FROM habits WHERE Habit_name=?", (Habit_name,))
    if cur.fetchone() is None:
        db.commit()
        return False
    else:
        return True
    

def habit_name_exist(db, Habit_name =''):
    cur = db.cursor()
    cur.execute("SELECT created FROM habits WHERE Habit_name=?" ("INSERT INTO created VALUES(datetime.now())", (Habit_name,)))
    db.commit()
    if cur.fetchone() is None:
        return False   
    else:
        return True







    
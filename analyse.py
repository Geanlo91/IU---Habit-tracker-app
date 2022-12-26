from db import *
from tracker import *
import click
import pytest

def get_habits_data(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    db = get_db()
    cur = db.cursor()
    cur.execute("ALTER TABLE habits ADD COLUMN (streak Integer, longest_streak Integer, success_rate Integer, completed text)")
    cur.execute("INSERT INTO habits VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (streak, longest_streak, success_rate, completed))

def calculate_streak(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    
    cur = db.cursor()
    cur.execute("SELECT streak FROM habits")
    if Periodicity == "Daily":
        streak = streak + 1
        return streak
    else:
        for streak in range(1, 8):
            streak = 1
            return streak
        for streak in range(8, 15):
            streak = 2
            return streak   
        for streak in range(15, 22):
            streak = 3
            return streak
        for streak in range(22, 29):
            streak = 4
            return streak   
        for streak in range(29, 36):
            streak = 5
            return streak
        for streak in range(36, 43):
            streak = 6
            return streak
        for streak in range(43, 50):
            streak = 7
            return streak
        for streak in range(50, 57):
            streak = 8
            return streak



def weekly_habits_list(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Periodicity = 'weekly'")
    return cur.fetchall()


def daily_habits_list(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Periodicity = 'daily'")
    return cur.fetchall()

def longest_streak_habit(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits where longest_streak = (SELECT MAX(longest_streak) FROM habits")
    return cur.fetchone()


def specific_habit(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name = ?", (Habit_name,))
    return cur.fetchone()

def view_success_rate(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits order by success_rate DESC")
    return cur.fetchall()


def get_habit_streak(db, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
    cur = db.cursor()
    cur.execute("SELECT streak FROM habits where Habit_name = ?", (Habit_name,))
    return cur.fetchone()
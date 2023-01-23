from db import *
from tracker import *
import click
 

def weekly_habits_list(Habit_name):
    '''
    This function shows all habits with a Weekly Periodicity in a table format.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Periodicity = 'Weekly'")
    result = cur.fetchall()
    if result is not None:
        print(tabulate(result, headers=["Habit name", "Created", "Start date", "Periodicity", "Run duration", "Checked", "Streak", "Longest streak", "Completed"], tablefmt="grid"))
    else:
        print("No weekly habits available")
        


def daily_habits_list(Habit_name):
    '''
    This function shows all habits with a Daily Periodicity in a table format.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Periodicity = 'Daily'")
    result =  cur.fetchall()
    if result is not None:
        print(tabulate(result, headers=["Habit name", "Created", "Start date", "Periodicity", "Run duration", "Checked", "Streak", "Longest streak", "Completed"], tablefmt="grid"))
    else:
        print("No Daily habits available")



def longest_streak_habit(Habit_name):
    '''
    This function shows the habit with the longest streak in a table format.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE longest_streak = (SELECT MAX(longest_streak) FROM habits)"), (Habit_name,)
    result = cur.fetchall()
    print(tabulate(result, headers=["Habit name", "Created", "Start date", "Periodicity", "Run duration", "Checked", "Streak", "Longest streak", "Completed"], tablefmt="grid"))




def get_habit_streak(Habit_name):
    '''
    This function shows a habit's streak value.
    '''
    db = get_db()
    cur = db.cursor()
    Habit_name = input("Enter the name of the habit you want to view the streak of: ")
    cur.execute("SELECT streak FROM habits WHERE Habit_name = ?", (Habit_name,))
    return cur.fetchone()
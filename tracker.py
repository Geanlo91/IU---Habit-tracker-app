from db import *
from datetime import date
import math

class track_habit:
    def __init__(self, Habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed):
        self.Habit_name = Habit_name
        self.created = created
        self.start_date = start_date
        self.Periodicity = Periodicity
        self.Run_duration = Run_duration
        self.streak = streak
        self.longest_streak = longest_streak
        self.success_rate = success_rate
        self.completed = completed

    def add (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == False:
            add_habit(db, self.Habit_name, self.created, self.start_date, self.Periodicity, self.Run_duration, self.streak, self.longest_streak, self.success_rate, self.completed)
            print("Habit added!")
        else:
            print("Habit already exists!")

    def created (self):
        db = get_db()
        if habit_name_exist (db, self.Habit_name) == True:
            add_habit(db, self.Habit_name)
            print("Habit created!")
        else:
            print("Habit already exists!")


    def delete (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            delete_habit(db, self.Habit_name)
            print("Habit deleted!")
        else:
            print("Habit doesn't exist!")

    def edit (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            edit_habit(db, self.Habit_name, self.created, self.start_date, self.Periodicity, self.Run_duration)
            print("Habit edited!")
        else:
            print("Habit doesn't exist!")

    def complete (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            complete_habit(db, self.Habit_name, self.completed)
            print("Habit completed!")
        else:
            print("Habit doesn't exist!")


    def reset (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            self.db = reset_habit(db, self.Habit_name, self.streak, self.longest_streak, self.success_rate, self.completed)
            print("Habit reset!")
        else:
            print("Habit doesn't exist!")


    def show (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            print("Habit name: ", self.Habit_name)
        else:
            print("Habit doesn't exist!")
       

    def tick_off (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            check_off_habit(db, self.Habit_name, self.streak, self.longest_streak, self.success_rate, self.completed)
            print("Habit ticked off!")
        else:
            print("Habit doesn't exist!")


    def get (self):
        db = get_db()
        if habit_exist_check(db, self.Habit_name) == True:
            return get_habit(db, self.Habit_name)
        else:
            print("Habit doesn't exist!")
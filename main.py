from datetime import date
from tracker import *
from db import *
from analyse import *
from tabulate import tabulate
import sqlite3
import click

#Creating the main menu
def main ():
    print("Welcome to Habits tracker!")
    print("Choose one of the following options:")
    print("1. Create a new habit")
    print("2. Manage habits")
    print("3. Analyse habits")
    print("4. Exit")

    choice = click.prompt("Enter your choice", type=int)

    # Creating a new habit
    if choice == 1:
        db = get_db()
        habit_name = str(input("Name of the Habit: "))
        if habit_name_exist (db, habit_name) == True:
            print("Habit already exists!")
        else:
            year = int(input('Enter created year: '))
            month = int(input('Enter created month: '))
            day = int(input('Enter created day: '))
            created = str(date(year, month, day))
            start_date = str(input("Start date: "))
            Periodicity = str(input("Periodicity: "))
            Run_duration = int(input("Run duration: "))
            habit = track_habit(habit_name, created, start_date, Periodicity, Run_duration)
            habit.created()
            habit.show(tabulate())
            habit.save()   

    # Managing habits
    elif choice == 2:
        db = get_db()
        print(tabulate(get_habits(db)))
        print("Choose one of the following options:")
        print("1. Delete a habit")
        print("2. Reset a habit's progress")
        print("3. Edit a habit")
        print("4. tick a habit")
        print("4. Complete a habit")
        print("5. Home")

        choice = click.prompt("Enter your choice", type=int)

        # Deleting a habit
        if choice == 1:
            habit_name = str(input("Name of the Habit: "))
            if habit_name_exist (db, habit_name) == True:
                delete_habit(db, habit_name)
            else:
                print("Habit does not exist!")

        # Resetting a habit's progress
        elif choice == 2:
            habit_name = str(input("Name of the Habit: "))
            if habit_name_exist (db, habit_name) == True:
                reset_habit(db, habit_name)
            else:
                print("Habit does not exist!")


        # Editing a habit's name
        elif choice == 3:
            habit_name = str(input("Name of the Habit: "))
            if habit_name_exist (db, habit_name) == True:
                edit_habit(db, habit_name)
            else:
                print("Habit does not exist!")

        # Ticking a habit by ticking on the calendar date
        elif choice == 4:
            habit_name = str(input("Name of the Habit: "))
            if habit_name_exist (db, habit_name) == True:
                check_off_habit(db, habit_name)
            else:
                print("Habit does not exist!")

        # Completing a habit by inputting Yes or No
        elif choice == 5:
            habit_name = str(input("Name of the Habit: "))
            if habit_name_exist (db, habit_name) == True:
                complete_habit(db, habit_name)
            else:
                print("Habit does not exist!")

        # Going back to the main menu
        elif choice == 6:
            main()

    #Analyse progress of habits
    elif choice == 3:
        db = get_db()
        print(tabulate(get_habits(db)))
        print("Choose one of the following options:")
        print("1. Show all habits")
        print("2. Show all habits with a Daily Periodicity")
        print("3. Show all habits with a Weekly Periodicity")
        print("4. Show a habit's streak")
        print("5. Show habit with the longest streak")
        print("6. Home")

        choice = click.prompt("Enter your choice", type=int)

        # Showing all habits in a table
        if choice == 1:
            db = get_db()
            print(tabulate(get_habits(db)))

        # Showing all habits with a Daily Periodicity in a table
        elif choice == 2:
            db = get_db()
            print(tabulate(daily_habits_list(db)))

        # Showing all habits with a Weekly Periodicity in a table
        elif choice == 3:
            db = get_db()
            print(tabulate(weekly_habits_list(db)))

        # Showing a habit's streak value
        elif choice == 4:
            db = get_db()
            print(get_habit_streak(db))

        # Showing the habit with the longest streak in a table format
        elif choice == 5:
            db = get_db()
            print(tabulate(longest_streak_habit(db)))

        # Going back to the main menu
        elif choice == 6:
            main()
    
    # Exiting the program
    elif choice == 4:
        print("Goodbye!")
        exit()

# If the user enters a number that is not in the menu, the program will remain in the main menu
if __name__ == "__main__":
    main()

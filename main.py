from datetime import date
from tracker import track_habit
from db import (get_db, habit_exist_check, add_habit, delete_habit, edit_habit, complete_habit, reset_habit, get_habits, prehabits)
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
    if choice not in [1,2,3,4]:
        print("Invalid choice. Please enter a valid choiCe.")
        main()
    

    # Creating a new habit
    if choice == 1:
        print("see example of habits below")
        db = get_db()
        print(tabulate(prehabits))
        print ("Enter your own habits")
        habit_name = str(input("Name of the Habit: "))
        print(habit_name)
        if habit_exist_check (habit_name):
            print("Habit already exists!")
            main()
        else:
            from datetime import datetime
            created = str(datetime.now().strftime("%Y-%m-%d"))
            start_date = str(input("Start date YYYY-MM-DD: "))
            accepted_periodicity = ["Daily", "Weekly"]
            Periodicity = input("Enter the new periodicity (Daily, Weekly):")
            while Periodicity not in accepted_periodicity:
                print("Invalid periodicity")
                Periodicity = input("Enter the new periodicity (Daily, Weekly):")
            Run_duration = int(input("Run duration: "))
            streak = 0
            longest_streak = 0
            success_rate = 0
            completed = "No"
            habit = track_habit(habit_name, created, start_date, Periodicity, Run_duration, 0, 0, 0, "No")
            add_habit(habit_name, created, start_date, Periodicity, Run_duration, streak, longest_streak, success_rate, completed)
            habit.show()
            habit.save()   
            main()

        
    # Managing habits
    elif choice == 2:
        db = get_db()
        print(tabulate(get_habits()))
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
            db = get_db()
            if habit_exist_check (habit_name) == True:
                delete_habit(habit_name)
                print("Habit " + habit_name + " has been deleted!")
                print(tabulate(get_habits()))
                main()
            else:
                print("Habit does not exist!")
                main()

        # Resetting a habit's progress
        elif choice == 2:
            print(tabulate(get_habits()))
            habit_name = str(input("Name of the Habit: "))
            db = get_db()
            if habit_exist_check (habit_name) == True:
                reset_habit(habit_name)
                updated_habit = get_habit(habit_name)
                print(updated_habit)
            else:
                print("Habit does not exist!")
            main()


        # Editing a habit's name
        elif choice == 3:
            habit_name = str(input("Name of the Habit: "))
            db = get_db()
            if habit_exist_check (habit_name) == True:
                edit_habit(habit_name)
                edited_habit = get_habit(habit_name)
                print(edited_habit)
            else:
                print("Habit does not exist!")
            main()

        # Ticking a habit by ticking on the calendar date
        elif choice == 4:
            habit_name = str(input("Name of the Habit: "))
            db = get_db()
            if habit_exist_check (habit_name) == True:
                check_off_habit(habit_name)
                checked_off = get_habit(habit_name)
                print(checked_off)
            else:
                print("Habit does not exist!")
                main()

        # Completing a habit by inputting Yes or No
        elif choice == 5:
            habit_name = str(input("Name of the Habit: "))
            db = get_db()
            if habit_exist_check (habit_name) == True:
                complete_habit(habit_name)
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
        if choice not in [1,2,3,4,5,6]:
            print("Invalid choice. Please enter a valid choise.")
            main()

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




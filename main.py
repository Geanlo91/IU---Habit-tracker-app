from datetime import date
from tracker import track_habit
from db import (get_db, habit_exist_check, add_habit, delete_habit, edit_habit, complete_habit, reset_habit, get_habits, prehabits)
from analyse import *
from tabulate import tabulate
import sqlite3
import click

#Creating the main menu
def main ():
    '''
    Main menu containing the functions of the app and its submenus. 
    In each chosen option, the user is prompted to enter the required information via the command line.
    '''
    print("Welcome to Habits tracker!")
    print("Choose one of the following options:")
    print("1. Create a new habit")
    print("2. Manage habits")
    print("3. Analyse habits")
    print("4. Exit")

    choice = click.prompt("Enter your choice", type=int)
    if choice not in [1,2,3,4]:
        print("Invalid choice. Please enter a valid choice.")
        main()
    

    # Creating a new habit
    if choice == 1:
        db = get_db()
        print("Do you want to see examples of habits? (Y/N)")
        choice = input("Enter your choice: (Y/N) ").upper()
        if choice == "Y":
            print(tabulate(prehabits, headers=["Habit_name", "created", "start_date", "Periodicity", "Run_duration", "Checked", "streak", "longest_streak", "completed"], tablefmt='psql'))
        elif choice == "N":
            pass
        print ("Enter your own habit")
        Habit_name = input("Name of the Habit: ").title()
        print(Habit_name)
        if habit_exist_check (Habit_name):
            print("Habit already exists!")
            main()
        else:
            from datetime import datetime
            created = str(datetime.now().strftime("%Y-%m-%d"))
            start_date = str(input("Start date YYYY-MM-DD: ")).title()
            accepted_periodicity = ["Daily", "Weekly"]
            Periodicity = input("Enter the new periodicity (Daily, Weekly):").title()
            while Periodicity not in accepted_periodicity:  
                print("Invalid periodicity")
                Periodicity = input("Enter the new periodicity (Daily, Weekly):").title()
            Run_duration = int(input("Run duration: "))
            Checked = str(start_date)
            streak = 0
            longest_streak = 0
            completed = "No"
            habit = track_habit(Habit_name, created, start_date, Periodicity, Run_duration, Checked, 0, 0, "No")
            add_habit(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed)
            habit.show()
            habit.save()   
            main()

        
    # Managing habits
    elif choice == 2:
        db = get_db()
        print("Choose one of the following options:")
        print("1. Edit a habit")
        print("2. tick a habit")
        print("3. Complete a habit")
        print("4. Delete a habit")
        print("5. Reset a habit's progress")
        print("6. Home")

        choice = click.prompt("Enter your choice", type=int)

        # Editing a habit's attributes
        if choice == 1:
            print(tabulate(get_habits()))
            Habit_name = str(input("Name of the Habit: ")).title()
            db = get_db()
            if habit_exist_check (Habit_name) == True:
                completed = get_completed_habits(Habit_name)
                edit_habit(Habit_name)
                edited_habit = get_habit(Habit_name)
                print(tabulate(edited_habit))
            else:
                print("Habit does not exist!")
            main()


        # Ticking a habit day/week by inputting the Habit_name and current Periodicity then the Checked attribute is automatically updated to the current date
        elif choice == 2:
            print(tabulate(get_habits()))
            Habit_name = str(input("Name of the Habit: ")).title()
            db = get_db()
            if habit_exist_check (Habit_name):
                cur = db.cursor()
                cur.execute("SELECT Periodicity FROM habits WHERE Habit_name = ?", (Habit_name,))
                Periodicity = cur.fetchone()[0]
                Checked = str(date.today())
                check_off_habit(Habit_name, Periodicity,Checked)
                checked_off = get_habit(Habit_name)
                print(tabulate(checked_off))
                main()
            else:
                print("Habit does not exist!")
                main()
            
            



        # Completing a habit. By inputting the Habit_name, the completed attribute is changed to "Yes" and the completed_date is added to the completed_habits table
        elif choice == 3:
            print(tabulate(get_habits()))
            Habit_name = str(input("Name of the Habit: ")).title()
            db = get_db()
            if habit_exist_check (Habit_name) == True:
                complete_habit(Habit_name)
                completed_habit = get_completed_habits(Habit_name)
                print(tabulate(completed_habit, headers=["Habit_name","Completed_date"], tablefmt='psql'))
                main()
            else:
                print("Habit does not exist!")
                main()


        # Deleting a habit
        elif choice == 4:
            print(tabulate(get_habits()))
            Habit_name = str(input("Name of the Habit: ")).title()
            db = get_db()
            if habit_exist_check (Habit_name) == True:
                delete_habit(Habit_name)
                print("Habit " + Habit_name + " has been deleted!")
                print(tabulate(get_habits()))
                main()
            else:
                print("Habit does not exist!")
                main()

        # Resetting a habit's progress
        elif choice == 5:
            print(tabulate(get_habits()))
            Habit_name = str(input("Name of the Habit: ")).title()
            db = get_db()
            if habit_exist_check (Habit_name) == True:
                reset_habit(Habit_name)
                updated_habit = get_habit(Habit_name)
                print(tabulate(updated_habit))
                main()
            else:
                print("Habit does not exist!")
            main()


        # Going back to the main menu
        elif choice == 6:
            main()


    #Analyse progress of habits
    elif choice == 3:
        db = get_db()
        allhabits = get_habits()
        print(tabulate(allhabits))
        print("Choose one of the following options:")
        print("1. Show all habits")
        print("2. Show all habits with a Daily Periodicity")
        print("3. Show all habits with a Weekly Periodicity")
        print("4. Show a habit's streak")
        print("5. Show habit with the longest streak") 
        print("6. Home")

        choice = click.prompt("Enter your choice", type=int)
        if choice not in [1,2,3,4,5,6]:
            print("Invalid choice. Please enter a valid choice.")
            main()

        # Showing all habits in a table
        if choice == 1:
            db = get_db()
            all_habits = get_habits()
            print(tabulate(all_habits,headers=["Habit_name", "created", "start_date", "Periodicity", "Run_duration", "Checked", "streak", "longest_streak", "completed"], tablefmt="grid"))
            

        # Showing all habits with a Daily Periodicity in a table
        elif choice == 2:
            db = get_db()
            daily = daily_habits_list(db)
            main()
        

        # Showing all habits with a Weekly Periodicity in a table
        elif choice == 3:
            db = get_db()
            weekly = weekly_habits_list(db)
            main()


        # Showing a habit's streak value
        elif choice == 4:
            db = get_db()
            streak_habit = get_habit_streak(Habit_name="Habit_name")
            print(streak_habit)
            main()

        # Showing the habit with the longest streak in a table format
        elif choice == 5:
            db = get_db()
            long_streak = longest_streak_habit(Habit_name="Habit_name")
            main()

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




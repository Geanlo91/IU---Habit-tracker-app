import sqlite3 
from datetime import date, datetime
from tabulate import tabulate
conn = sqlite3.connect("main.db")
import pandas as pd
from datetime import timedelta


def get_db(name="main.db"):
    '''
    Defining the database and its name (main.db)
    '''
    db = sqlite3.connect(name)
    create_tables(db) 
    return db


def create_tables(db):
    '''
    Creating the habit table in the database that will house all created habits.
    '''
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habits(
        Habit_name TEXT PRIMARY KEY,
        created TEXT,
        start_date TEXT,
        Periodicity TEXT,
        Run_duration INTEGER,
        Checked DATE, 
        streak INTEGER, 
        longest_streak INTEGER, 
        completed TEXT
    )""")
    db.commit()
    return db



def add_habit(Habit_name, created, start_date, Periodicity, Run_duration, Checked, streak, longest_streak, completed):
    '''
    First checking if the habit already exists in the database. If it does, the user is notified and the function ends. If it doesn't, the habit is added to the database and the table is updated.
    '''
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
    '''
    Editing a habit's start date, periodicity and run duration. This is only possible if the habit is still active and not completed. 
    User input the Periodicity and Run_duration. 
    The start date is automatically set to the current date. The table is updated.
    '''
    db = get_db()
    cur = db.cursor()
    from datetime import datetime
    cur.execute("SELECT completed FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
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
        cur.execute("UPDATE habits SET start_date=?, Periodicity=?, Run_duration=? WHERE Habit_name=?",
    (start_date, Periodicity, Run_duration, Habit_name))
        db.commit()



def delete_habit(Habit_name):
    '''
    Deleting a habit from the database.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE Habit_name=?", (Habit_name,))
    db.commit()



def complete_habit(Habit_name):
    '''
    Ending tracking of a habit. 
    The habit is marked as completed and the table is updated.
    Another table is created to store the date the habit was completed.
    '''
    db = get_db()
    cur = db.cursor()
    completed = "Yes"
    cur.execute("SELECT completed FROM habits Where Habit_name=?",(Habit_name,))
    result = cur.fetchone()
    if result is not None and result[0] == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        cur.execute("""CREATE TABLE IF NOT EXISTS Completed_habits (Habit_name TEXT, Completed_date DATE, CONSTRAINT fk_habit_name FOREIGN KEY (Habit_name) REFERENCES habits(Habit_name))""")
        db.commit()
        cur.execute("UPDATE habits SET completed=? WHERE Habit_name=?", (completed, Habit_name))
        db.commit()
        current_date = datetime.today()
        cur.execute("SELECT * FROM Completed_habits WHERE Habit_name=?", (Habit_name,))
        result = cur.fetchone()
        if result is None:
            cur.execute("INSERT INTO Completed_habits VALUES(?, ?)", (Habit_name, current_date))
            db.commit()
        else:
            cur.execute("UPDATE Completed_habits SET Completed_date=? WHERE Habit_name=?", (current_date, Habit_name))
            db.commit()
        


def reset_habit(Habit_name):
    '''
    Resetting the streak and longest streak of a habit to zero and marking it as not completed.
    '''
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
    
    

def check_off_habit(Habit_name, Periodicity,Checked):
    '''
    Marking a habit as completed for the day/week. Daily habits can only be marked as completed once a day. 
    Weekly habits can only be marked as completed once a week. 
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT completed FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
    completed = result[0]
    if completed == "Yes":
        print("Habit has already been completed and cannot be edited")
    else:
        cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name,))
        result = cur.fetchone()
        if result is None:
            raise ValueError("Habit does not exist")

        previously_checked = result[5]
        current_streak = result[6]
        long_streak = int(result[7])
        
        
        from datetime import datetime, date
        format = "%Y-%m-%d"
        previously_checked_2 = date.fromisoformat(previously_checked)


        if Periodicity == "Daily":
            from datetime import timedelta
            if previously_checked_2 + timedelta(days=1) == date.fromisoformat(Checked):
                current_streak += 1
                Checked = date.today()
            elif previously_checked_2 + timedelta(days=1) > date.today():
                current_streak == current_streak
                Checked = date.today()
            else:
                current_streak = 1
                Checked = date.today()

        elif Periodicity == "Weekly":
            from datetime import timedelta
            if previously_checked_2 + timedelta(days=7) == date.today():
                current_streak += 1
                Checked = date.today() 
            elif previously_checked_2 + timedelta(days=7) > date.today():
                current_streak == current_streak
                Checked = previously_checked
            else:
                current_streak = 1
                Checked = previously_checked

        else:
            raise ValueError("Invalid periodicity")

        if current_streak > long_streak:
            long_streak = current_streak

        cur.execute("UPDATE habits SET streak=?, Checked=?, longest_streak=? WHERE Habit_name=?",(current_streak, Checked, long_streak, Habit_name))

        if current_streak >= int(result[4]):
            cur.execute("UPDATE habits SET completed=? WHERE Habit_name=?", ("Yes", Habit_name))
        db.commit()
    




def get_habits():
    '''
    A view of all the habits saved in the database whether completed or not.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    db.commit()
    return cur.fetchall()


def get_habit(Habit_name):
    '''
    A view of a specific habit saved in the database. Search is done by habit name.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name,))
    db.commit()
    return cur.fetchall()


def habit_exist_check(Habit_name):
    '''
    Checking if a habit exists in the database and the habits table.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", [Habit_name])
    habit = cur.fetchone()
    if habit:
        return True
    else:
        return False



def get_completed_habits(Habit_name):
    '''
    Getting a completed habit from the database and the table that only stores completed habits.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM Completed_habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchall() 
    return result


def get_periodicity(Habit_name):
    '''
    Getting the periodicity of a habit from the database.
    This does not return all the elements of the habit but just the string that represents the periodicity.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT Periodicity FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
    return result


def get_checked(Habit_name):
    '''
    Getting the last date a habit was checked from the database.
    This does not return all the elements of the habit but just the string that represents the Checked column in the table.
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT Checked FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
    return result



def due_date_reached(Habit_name):
    '''
    Checking if the due date of a habit has been reached.
    When the date has been reached and user does not Compete the habit, 
    this automatically completes the habit. 
    The difference between the current date and the start date is calculated and compared to the habit's run duration.
    If the difference is greater than the run duration, the habit is completed.
    '''
    db = get_db()
    cur = db.cursor()
    from datetime import date, datetime, timedelta
    cur.execute("SELECT * FROM habits WHERE Habit_name=?", (Habit_name,))
    result = cur.fetchone()
    if result is None:
        raise ValueError("Habit does not exist")
    else:
        start_date = datetime.strptime(result[1], '%Y-%m-%d').date()
        Run_duration = result[4]
        current_date = date.today()

        difference = current_date - start_date

        if difference.days > Run_duration:
            cur.execute("UPDATE habits SET completed = 'Yes' WHERE Habit_name=?",(Habit_name,))
            db.commit()
            return True
        else:
            return False
            

 

#This saves as an example for the user on what to input when creating a habit and what the tables will look like
prehabits = [
    ['Running', '2021-01-01', '2022-11-01', 'Daily',45,'2021-01-02', 5, 7, 'No'],
    ['Reading', '2021-01-01', '2022-10-01', 'Weekly' ,30,'2022-10-25', 5,10, 'No'],
    ['Meditation', '2023-01-01', '2023-01-01', 'Daily', 30,'2023-01-20', 6, 10, 'Yes'],
    ['Playing Soccer', '2021-01-01', '2023-01-01', 'Weekly', 5,'2023-01-02', 1, 2, 'No'],
    ['Rock climbing', '2021-01-01', '2023-01-01', 'Daily',60,'2023-10-02', 10, 10, 'No']]



    




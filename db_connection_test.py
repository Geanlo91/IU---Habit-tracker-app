from db import *
import os

db_name = "main.db"
if os.path.exists(db_name):
    db = sqlite3.connect(db_name)
else:
    print("Database does not exist")


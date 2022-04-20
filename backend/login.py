import sqlite3
from datetime import datetime as dt

def connect_to_database():
    """Connects to the database where the log in information is held."""

    return sqlite3.connect("data/login_info_database.db")

def get_cursor(connection):
    """Creates a cursor for the database connection."""

    return connection.cursor()

def table_exists(cursor):
    """Checks whether the login_data table already exists or not."""

    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='login_data'""")
    result = cursor.fetchone()

    return True if len(result) > 0 else False

def create_table(connection, cursor):
    """Creates a table in the database for the login info and populates it."""
    
    # Create table and define the fields:
    cursor.execute("""CREATE TABLE login_data
    (username TEXT, password TEXT)""")

    #Add valid user login to database and save:
    cursor.execute("""INSERT INTO login_data
    VALUES (?,?)""", ["user123", "pa55w0rd"])
    connection.commit()

if __name__ == "__main__":

    # Connect to the database and get the cursor:
    connection = connect_to_database()
    cursor = get_cursor(connection)

    # Check if there are any tables in the database and if not create one:
    if not table_exists(cursor):
        create_table(connection, cursor)

    user_attempt = input("Username: ")
    password_attempt = input("Password: ")

    # Checking credentials given are valid:
    cursor.execute("""SELECT username, password FROM login_data where username=?""", [user_attempt])
    results = cursor.fetchall()
    if len(results) > 0:
        print("User found.")
        password = results[0][1]
        if password_attempt == password:
            print("Login successful.")
            # Get current time, format into <day> <month> <year> <hh:mm:ss>:
            current_time = dt.now().strftime("%d %b %Y %H:%M:%S") 
            print(f"Logged in at {current_time}.")
        else:
            print("Login failed: incorrect password.")
    else:
        # Assume each user is unique (only created 1!):
        print("Login failed: user not found.")


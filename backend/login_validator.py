import ntplib
import sqlite3
from time import ctime

def get_time_from_server():
    """Gets the current time from the time server using NTP."""
    response = c.request('europe.pool.ntp.org', version=3)
    
    return ctime(response.tx_time)

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

def get_last_login_date():
    """Gets the last login date from the last_login.txt file."""

    with open("data/last_login.txt", "r") as file:
        content = file.readlines()
        # For a first time login, there won't be a date, but there will be one for subsequent logins:
        if len(content) > 0:
            date = content[0]
        else:
            # First login case - there is no date:
            date = ""
    
    return date

def set_last_login_date(date):
    """Writes the last login date into the last_login.txt file, overriding the previous date present."""

    with open("data/last_login.txt", "w") as file:
        file.write(date)


if __name__ == "__main__":

    # Displaying current time using a time server:
    # Open connection to server:
    c = ntplib.NTPClient()
    current_time = get_time_from_server()
    print(current_time) # *Needs to be sent to frontend*

    # Connect to the database and get the cursor:
    connection = connect_to_database()
    cursor = get_cursor(connection)

    # Check if there are any tables in the database and if not create one:
    if not table_exists(cursor):
        create_table(connection, cursor)

    user_attempt = input("Username: ") # *Needs to be retrieved from frontend*
    password_attempt = input("Password: ") # *Needs to be retrieved from frontend*

    # Checking credentials given are valid:
    cursor.execute("""SELECT username, password FROM login_data where username=?""", [user_attempt])
    results = cursor.fetchall()
    if len(results) > 0:
        print("User found.")
        password = results[0][1]
        if password_attempt == password:
            print("Login successful.")
            # Get current login time, using the time server:
            current_login_time = get_time_from_server()
            last_login = get_last_login_date() 
            print(f"Last logged in at {last_login}.") # *Needs to be sent to frontend*
            set_last_login_date(current_login_time)
        else:
            print("Login failed: incorrect password.")
    else:
        # Assume each user is unique (only created 1!):
        print("Login failed: user not found.")


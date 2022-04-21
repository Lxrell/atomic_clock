import ntplib
import sqlite3
from time import ctime

class Login():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False

    def get_time_from_server(self):
        """Gets the current time from the time server using NTP."""
        
        # Open connection to time server and get time:
        c = ntplib.NTPClient()
        response = c.request('europe.pool.ntp.org', version=3)
        
        return ctime(response.tx_time)

    def connect_to_database(self):
        """Connects to the database where the log in information is held."""

        return sqlite3.connect("data/login_info_database.db")

    def get_cursor(self, connection):
        """Creates a cursor for the database connection."""

        self.connection = connection

        return self.connection.cursor()

    def table_exists(self, cursor):
        """Checks whether the login_data table already exists or not."""

        self.cursor = cursor

        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='login_data'""")
        result = self.cursor.fetchone()

        return True if len(result) > 0 else False

    def create_table(self, connection, cursor):
        """Creates a table in the database for the login info and populates it."""

        self.connection = connection
        self.cursor = cursor
        
        # Create table and define the fields:
        self.cursor.execute("""CREATE TABLE login_data
        (username TEXT, password TEXT)""")

        #Add valid user login to database and save:
        self.cursor.execute("""INSERT INTO login_data
        VALUES (?,?)""", ["user123", "pa55w0rd"])
        self.connection.commit()

    def get_last_login_date(self):
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

    def set_last_login_date(self, date):
        """Writes the last login date into the last_login.txt file, overriding the previous date present."""

        self.date = date

        with open("data/last_login.txt", "w") as file:
            file.write(self.date)

    def login_attempt(self, cursor, user_attempt, password_attempt):
        """Checks the given credentials match those in the database; if login successful will print last login date and set last login date for next time."""
        
        self.cursor = cursor
        self.user_attempt = user_attempt
        self.password_attempt = password_attempt
        
        self.cursor.execute("""SELECT username, password FROM login_data where username=?""", [self.user_attempt])
        results = self.cursor.fetchall()
        if len(results) > 0:
            # I am sssuming each user is unique (only created 1 in database!):
            # results is a list of tuples (username, password):
            password = results[0][1]
            if self.password_attempt == password:
                # Get current login time, using the time server:
                current_login_time = self.get_time_from_server()
                last_login = self.get_last_login_date() 
                self.set_last_login_date(current_login_time)
                self.logged_in = True
                return f"Login successful. Last logged in at {last_login}." # *Needs to be sent to frontend*   
            else:
                return "Login failed: incorrect password."
        else:
            return "Login failed: user not found."

if __name__ == "__main__":

    # Using user input to simulate getting login details from frontend:
    user_attempt = input("Username: ") # *Needs to be retrieved from frontend*
    password_attempt = input("Password: ") # *Needs to be retrieved from frontend*

    # Create a new login instance for when someone tries to log in:
    new_login = Login(user_attempt, password_attempt)

    # Connect to the database and get the cursor:
    connection = new_login.connect_to_database()
    cursor = new_login.get_cursor(connection)

    # Check if there are any tables in the database and if not create one:
    if not new_login.table_exists(cursor):
        new_login.create_table(connection, cursor)

    # Attempt the login with the given credentials:
    result = new_login.login_attempt(cursor, user_attempt, password_attempt)
    print(result) # *Needs to be sent to frontend*

    # Displaying current time using a time server if we are logged in:
    if new_login.logged_in == True:
        # Time server request may time out and raise an exception:
        try:
            # Get and display current time from server:
            current_time = new_login.get_time_from_server()
            print(f"The current time is {current_time}.") # *Needs to be sent to frontend*
        except ntplib.NTPException:
            print("No response was received from the server.")

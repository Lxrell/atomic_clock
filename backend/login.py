import sqlite3

# Connect to the database with the login info and create a cursor:
connection = sqlite3.connect("database/login_info.db")
cursor = connection.cursor()

# Creating a table in the database:
#cursor.execute("""CREATE TABLE login_data
#(username TEXT, password TEXT)""")

# Add login value to database and save:
#cursor.execute("""INSERT INTO login_data
#VALUES (?,?)""", ['user123', 'pa55w0rd'])
#connection.commit()

user_attempt = input("Username: ")
password_attempt = input("Password: ")

# Checking credentials given are valid:
check = cursor.execute("""SELECT username, password FROM login_data where username=?""", [user_attempt])
results = cursor.fetchall()
if len(results) > 0:
    print("User found.")
    password = results[0][1]
    if password_attempt == password:
        print("Login successful.")
    else:
        print("Login failed: incorrect password.")
else:
    # Deal with unique user problem elsewhere and assume there each user is unique:
    print("Login failed: user not found.")


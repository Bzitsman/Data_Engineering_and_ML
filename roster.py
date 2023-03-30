import json
import sqlite3

# Connect to the database
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()


# Create the User, Course, and Member tables
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER, -- Added role column
    PRIMARY KEY (user_id, course_id)
)
''')

# Prompt the user for the filename of the JSON data file
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data_sample.json'

# Read the JSON data from the file
str_data = open(fname).read()
json_data = json.loads(str_data)

# Loop through the JSON data and insert it into the database
for entry in json_data:
    # Extract the name, title, and role values from the current entry
    name = entry[0]
    title = entry[1]
    role = entry[2] # added

    # Print the values to confirm they are correct
    print((name, title, role))

    # Insert the user into the User table
    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )

    # Get the ID of the user that was just inserted
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    # Insert the course into the Course table
    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )

    # Get the ID of the course that was just inserted
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    # Insert the member into the Member table
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    # Commit the changes to the database
    conn.commit()

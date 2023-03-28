# import the SQLite3 module
import sqlite3

# create a connection object to a SQLite database and a cursor object to execute SQL commands
conn = sqlite3.connect('emaildba1.sqlite')
cur = conn.cursor()

# Drop the table if it already exists and create a new table to store email counts
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Prompt user for a file name or set the default file name
fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'

# Open the file and iterate through each line
fh = open(fname)
for line in fh:
    # Look for lines that start with 'From: '
    if not line.startswith('From: '): continue
    # Split the line into words and extract the email address
    pieces = line.split()
    email = pieces[1]
    # Split the email address into two parts: emailname and organization (based on the '@' symbol)
    (emailname, organization) = email.split('@')
   
    # Retrieve the current count for the given organization from the Counts table
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (organization, ))
    row = cur.fetchone()
    # If the organization is not yet in the Counts table, insert a new row with a count of 1
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) VALUES (?, 1)''', (organization, ))
    # If the organization is already in the Counts table, update its count by 1
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (organization, ))
# Commit all changes to the database (i.e., write them to disk)
conn.commit()

# Query the Counts table for the top 10 organizations with the most email messages and print the results
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
print("Counts: ")
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

# Close the cursor and the database connection
cur.close()

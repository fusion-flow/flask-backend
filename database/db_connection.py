import sqlite3

# Step 1: Connect to the database (or create a new one)
conn = sqlite3.connect('fusionFlow_db.db')

# Step 2: Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Step 3: Execute SQL commands to create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urlMapping (
        id INTEGER PRIMARY KEY,
        intent TEXT NOT NULL,
        url TEXT NOT NULL
    )
''')

# Step 4: Commit the changes and close the connection
conn.commit()
conn.close()

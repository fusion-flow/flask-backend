import sqlite3

# Step 1: Connect to the database (or create a new one)
conn = sqlite3.connect('fusionFlow_db.db')

# Step 2: Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Example data to insert
data_to_insert = [
    ('Resource page', 'resource-categories'),
    ('Therapy Support', 'resource-categories/therapy'),
    ('Tech support', 'resource-categories/help-with-technology'),
    ('Emotion support', 'resource-categories/emotions-and-social-life')
    # Add more rows as needed
]

# Execute the SQL INSERT statement with executemany
cursor.executemany("INSERT INTO urlMapping (intent, url) VALUES (?, ?)", data_to_insert)


# Step 4: Commit the changes and close the connection
conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("projects.db")
cursor = conn.cursor()

# Show table schema
cursor.execute("PRAGMA table_info(my_projects)")
for col in cursor.fetchall():
    print(col)

import sqlite3
from sqlalchemy import create_engine, text
import os
from urllib.parse import quote_plus

# 🔹 MySQL credentials from environment
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("Database environment variables missing")

# 🔹 Connect to MySQL
mysql_engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# 🔹 Connect to old SQLite
sqlite_conn = sqlite3.connect("projects.db")
sqlite_cursor = sqlite_conn.cursor()

# 🔹 Fetch old data
sqlite_cursor.execute("SELECT id, title, date, description, skills_practiced, github_repo FROM my_projects")
rows = sqlite_cursor.fetchall()

print(f"Found {len(rows)} rows in SQLite database.")

# 🔹 Insert into MySQL
with mysql_engine.begin() as conn:  # begin a transaction
    for row in rows:
        # If date is stored as string, you may need to convert to proper datetime
        conn.execute(
            text("""
            INSERT INTO my_projects (id, title, date, description, skills_practiced, github_repo)
            VALUES (:id, :title, :date, :description, :skills_practiced, :github_repo)
            """),
            {
                "id": row[0],
                "title": row[1],
                "date": row[2],
                "description": row[3],
                "skills_practiced": row[4],
                "github_repo": row[5],
            }
        )

print("✅ Migration complete!")

# 🔹 Close SQLite connection
sqlite_conn.close()

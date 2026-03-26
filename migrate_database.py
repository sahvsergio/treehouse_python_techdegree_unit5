#!/usr/bin/env python3
import os
from urllib.parse import quote_plus
import sqlite3
import pymysql
from sqlalchemy import create_engine, text

# -----------------------------
# 🔹 Environment variables
# -----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
SQLITE_FILE = "projects.db"  # path to your old SQLite file

# Safety checks
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("One or more MySQL environment variables are missing")

if not os.path.exists(SQLITE_FILE):
    raise RuntimeError(f"SQLite file '{SQLITE_FILE}' not found in project folder")

DB_PASSWORD_QUOTED = quote_plus(DB_PASSWORD)

# -----------------------------
# 🔹 Connect to MySQL
# -----------------------------
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_QUOTED}@{DB_HOST}/{DB_NAME}"
mysql_engine = create_engine(mysql_url)

# -----------------------------
# 🔹 Connect to SQLite
# -----------------------------
sqlite_conn = sqlite3.connect(SQLITE_FILE)
sqlite_cursor = sqlite_conn.cursor()

# -----------------------------
# 🔹 Read data from SQLite
# -----------------------------
try:
    sqlite_cursor.execute("SELECT id, title, date, description, skills_practiced, github_repo FROM my_projects")
    rows = sqlite_cursor.fetchall()
    print(f"Found {len(rows)} rows in SQLite database")
except sqlite3.OperationalError as e:
    raise RuntimeError(f"Error reading SQLite database: {e}")

# -----------------------------
# 🔹 Insert into MySQL
# -----------------------------
with mysql_engine.begin() as conn:
    for row in rows:
        # row = (id, title, date, description, skills_practiced, github_repo)
        insert_query = text("""
            INSERT INTO my_projects (id, title, date, description, skills_practiced, url)
            VALUES (:id, :title, :date, :description, :skills_practiced, :url)
        """)
        conn.execute(insert_query, {
            "id": row[0],
            "title": row[1],
            "date": row[2],
            "description": row[3],
            "skills_practiced": row[4],
            "url": row[5]
        })

print("✅ Migration completed successfully")

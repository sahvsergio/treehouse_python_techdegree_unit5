import sqlite3
import os
import datetime
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, text

# 🔹 Environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("Database environment variables are missing")

# 🔹 Encode password for URL
DB_PASSWORD_QUOTED = quote_plus(DB_PASSWORD)

# 🔹 Connect to MySQL
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_QUOTED}@{DB_HOST}/{DB_NAME}"
engine = create_engine(mysql_url, future=True)

# 🔹 Drop table if exists (optional)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS my_projects;"))
    conn.commit()

# 🔹 Define new table schema
metadata = MetaData()

projects_table = Table(
    "my_projects",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255)),
    Column("date", DateTime, default=datetime.datetime.now),
    Column("description", String(500)),
    Column("skills_practiced", String(255)),
    Column("url", String(255)),
)

# 🔹 Create table in MySQL
metadata.create_all(engine)

# 🔹 Connect to old SQLite database
sqlite_conn = sqlite3.connect("projects.db")
sqlite_cursor = sqlite_conn.cursor()

# 🔹 Fetch all rows from old table
sqlite_cursor.execute("""
    SELECT id, Title, Date, Description, "Skills Practice", "GitHub Repo"
    FROM my_projects
""")
rows = sqlite_cursor.fetchall()

# 🔹 Insert rows into MySQL
with engine.connect() as conn:
    for row in rows:
        id_, title, date_str, description, skills, github = row

        # Convert string date to datetime if necessary
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                date = datetime.datetime.now()
        else:
            date = datetime.datetime.now()

        insert_stmt = projects_table.insert().values(
            id=id_,
            title=title,
            date=date,
            description=description,
            skills_practiced=skills,
            url=github
        )
        conn.execute(insert_stmt)
    conn.commit()  # commit all inserts

sqlite_conn.close()
print(f"✅ Migrated {len(rows)} projects from SQLite to MySQL")

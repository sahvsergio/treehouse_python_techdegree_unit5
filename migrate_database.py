import sqlite3
from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
import os
import datetime

# 🔹 Environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("Database environment variables are missing")

# 🔹 Encode password
DB_PASSWORD_QUOTED = quote_plus(DB_PASSWORD)

# 🔹 MySQL connection
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_QUOTED}@{DB_HOST}/{DB_NAME}"
engine = create_engine(mysql_url)

# 🔹 Connect to old SQLite
sqlite_conn = sqlite3.connect("projects.db

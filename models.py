from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from sqlalchemy import text
import datetime
import os

app = Flask(__name__, template_folder='templates')

# Environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))  # encode special chars
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Safety check
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("Database environment variables are missing or incorrect")

# SQLAlchemy connection string
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Test connection
def test_connection():
    try:
        with app.app_context():
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ MySQL connection successful:", result.scalar())
    except Exception as e:
        print("❌ MySQL connection failed:", e)

with app.app_context():
    db.create_all()
    print("✅ Tables created (if they didn't exist)")

test_connection()

# Correct model
class Project(db.Model):
    __tablename__ = 'my_projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String(500))
    skills_practiced = db.Column(db.String(255))
    url = db.Column(db.String(255))

    def __repr__(self):
        return (
            f"Project(Title: {self.title}, Date: {self.date}, "
            f"Description: {self.description}, Skills Practiced: {self.skills_practiced}, "
            f"Repo link: {self.url})"
        )

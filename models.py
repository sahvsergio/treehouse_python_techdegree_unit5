from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from urllib.parse import quote_plus

app = Flask(__name__, template_folder='templates')

# Environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("Database environment variables are not set")

# SQLAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'my_projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.String(255))
    date = db.Column('date', db.DateTime, default=datetime.datetime.now)
    description = db.Column('description', db.String(500))
    skills_practiced = db.Column('skills_practiced', db.String(255))
    url = db.Column('github_repo', db.String(255))

    def __repr__(self):
        return (
            f"Project("
            f"Title: {self.title}, "
            f"Date: {self.date}, "
            f"Description: {self.description}, "
            f"Skills Practiced: {self.skills_practiced}, "
            f"Repo link: {self.url})"
        )

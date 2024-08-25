"""Provide several sample math calculations.

This module allows the user to make mathematical calculations.

The module contains the following functions:

- `add(a, b)` - Returns the sum of two numbers.
- `subtract(a, b)` - Returns the difference of two numbers.
- `multiply(a, b)` - Returns the product of two numbers.
- `divide(a, b)` - Returns the quotient of two numbers.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

# create the and also assign the instance path to  the current directory
app = Flask(__name__, instance_path=f'{os.getcwd()}')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


class Project(db.Model):
    """
    A class used to represent a project

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    __tablename__ = 'my_projects'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    # timestamp when the item was created

    title=db.Column('Title', db.String())
    date = db.Column('Date',  db.DateTime, default=datetime.datetime.now)
    description=db.Column('Description', db.String())
    skills_practiced = db.Column('Skills Practice', db.String())
    url = db.Column('GitHub Repo', db.String())


# finish creating the fields here, before setting the site again
    def __repr__(self):

        """
        Prints what the animals name is and what sound it makes.

        If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """
        return f'''
    Project(
    Title:{self.title},
    Date:{self.date},
    Description: {self.description},
    Skills Practiced: {self.skills_practiced},
    Repo link: {self.url}
    '''
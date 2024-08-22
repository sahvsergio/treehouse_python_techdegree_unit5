#!/usr/bin/env python3.10
"""Provide several sample math calculations.

This module allows the user to make mathematical calculations.

The module contains the following functions:

- `add(a, b)` - Returns the sum of two numbers.
- `subtract(a, b)` - Returns the difference of two numbers.
- `multiply(a, b)` - Returns the product of two numbers.
- `divide(a, b)` - Returns the quotient of two numbers.
"""
# handling the database and models
import sqlalchemy
from sqlalchemy import create_engine, cast, func, or_, select
from sqlalchemy.orm import scoped_session, sessionmaker

# flask imports
from flask import flash, redirect, render_template, request, url_for
from models import Project, Flask, app, db
# create routes(visible parts of the site- urls)


@app.route('/', methods=['GET', 'POST'])
# decorator
def index():
    """Renders the index page of the app.

    Examples:
        >>> index()
        6.0
        >>> index()


    Args:
    none

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """
    return render_template('index.html')


if __name__ == '__main__':

    with app.app_context():
        # creating the engine
        engine = db.engine
        db.create_all()

    # making the app run, you just need to run the app.py file on the terminal
    # local app.run(debug=True , port=8000, host='127.0.0.1')
    # internet
    app.run(debug=True, port=8000, host='127.0.0.1')

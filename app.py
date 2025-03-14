"""Provide several sample math calculations.

This module allows the user to make mathematical calculations.

The module contains the following functions:

- `add(a, b)` - Returns the sum of two numbers.
- `subtract(a, b)` - Returns the difference of two numbers.
- `multiply(a, b)` - Returns the product of two numbers.
- `divide(a, b)` - Returns the quotient of two numbers.
"""
# handling the database and models

from flask import Flask
import sqlalchemy
from sqlalchemy import create_engine, cast, func, or_, select
from sqlalchemy.orm import scoped_session, sessionmaker

# flask imports
from flask import flash, redirect, render_template, request, url_for, flash, jsonify
from models import Project, Flask, app, db
import datetime


#flask-admin
from flask_admin import Admin


from flask_admin import form

from flask_bootstrap import Bootstrap

from flask_admin.contrib.sqla import ModelView


# create routes(visible parts of the site- urls)

# admin view
##

admin = Admin(app, name='Dashboard')







@app.route('/', methods=['GET', 'POST'])
# decorator
def index():
    '''
    index
    creates the entry point/home page for the site
    '''

    projects = db.session.query(Project).all()

    return render_template('index.html', projects=projects)



@app.route('/projects/new', methods=['GET', 'POST'])
def create():
    '''Turns the string into a date object'''
    # 'title', 'Hello'),
    # ('date', '2024-12'),
    # ('desc', 'Helloo'),
    # ('skills', 'Python'),
    # ('github', 'https://www.bloghorror.com')])
    projects = db.session.query(Project).all()
    if request.form:
        date_format = '%Y-%m'
        cleaned_date = datetime.datetime.strptime(
            request.form['date'],
            date_format
        )
        new_project = Project(
            title=request.form['title'],
            date=cleaned_date,
            description=request.form['desc'],
            skills_practiced=request.form['skills'],
            url=request.form['github']
        )
        db.session.add(new_project)
        print(db.session.dirty)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('new_project.html', projects=projects)


@app.route('/projects/<int:id>')
def detail(id):
    projects = db.session.query(Project).all()
    project = db.one_or_404(db.select(Project).filter_by(id=id))
    skills = project.skills_practiced

    return render_template('detail.html',
                           project=project,
                           id=id, skills=skills,
                           projects=projects)


@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit(id):

    projects = db.session.query(Project).all()
    project = db.one_or_404(db.select(Project).filter_by(id=id))
    if request.method == 'POST':
        if request.form:
            project.title = request.form['title']
            date_format = '%Y-%m'
            date = request.form['date']
            year, month = date.split('-')
            print(date)
            project.date = datetime.datetime.strptime(
                request.form['date'], '%Y-%m')
            project.description = request.form['desc']
            project.skills_practiced = request.form['skills']
            project.url = request.form['github']

            db.session.commit()

            return redirect(url_for('index'))
    return render_template('edit_project.html',
                           project=project,
                           projects=projects,
                           id=project.id,
                           date=datetime.datetime.strftime(
                               project.date.date(),
                               '%Y-%m')
                           )


@app.route('/projects/<int:id>/delete')
def delete(id):
    projects = db.session.query(Project).all()
    project = db.one_or_404(db.select(Project).filter_by(id=id))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    projects = db.session.query(Project).all()

    return render_template('about.html', projects=projects)


@app.errorhandler(404)
def not_found(error):
    projects = db.session.query(Project).all()
    return render_template('404.html', projects=projects), 404


if __name__ == '__main__':
    with app.app_context():
        # creating the engine
        engine = db.engine
        db.create_all()

    # making the app run, you just need to run the app.py file on the terminal
    # local app.run(debug=True , port=8000, host='127.0.0.1')
     #internet
    app.run( port=8000,debug=False, host='127.0.0.1')

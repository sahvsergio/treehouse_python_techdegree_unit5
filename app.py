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
import datetime


# create routes(visible parts of the site- urls)
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
    project=db.one_or_404(db.select(Project).filter_by(id=id))
    skills=project.skills_practiced
    
    return render_template('detail.html',project=project,  id=id, skills=skills )


@app.route('/projects/<id>/edit',methods=['GET', 'POST'])
def edit(id):
    project = db.one_or_404(db.select(Project).filter_by(id=id))
    
        
    if request.form:
        print(request.form)
        project.title= request.form['title']
        date_format = '%Y-%m'
        date= request.form['date']
        cleaned_date = datetime.datetime.strptime(
            request.form['date'], date_format)
        project.date=cleaned_date
        project.description = request.form['desc']
        project.skills_practiced = request.form['skills']
        project.url = request.form['github']
        
        db.session.commit()

        return redirect(url_for('index'))
    

    return render_template('edit_project.html', project=project)
    


@app.route('/projects/<id>/delete')
def delete(id):
    pass


if __name__ == '__main__':

    with app.app_context():
        # creating the engine
        engine = db.engine
        db.create_all()

    # making the app run, you just need to run the app.py file on the terminal
    # local app.run(debug=True , port=8000, host='127.0.0.1')
    # internet
    app.run(debug=True, port=8000, host='127.0.0.1')

# ------------------------
# CORE IMPORTS
# ------------------------
from flask import (
    abort, redirect, render_template,
    request, url_for, Response
)

from models import Project, app, db

# ------------------------
# ADMIN
# ------------------------
from flask_admin import Admin

# ------------------------
# UTILITIES
# ------------------------
import datetime
from io import StringIO
import csv

admin = Admin(app, name='My Portfolio Admin',  theme=Bootstrap4Theme(swatch='simplex'))
admin.add_view(ModelView(Project, db.session))







# ------------------------
# ROUTES
# ------------------------
@app.route('/')
def index():
    projects = db.session.query(Project).all()
    return render_template('index.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
def create():
    if not check_auth():
        return authenticate()

    projects = db.session.query(Project).all()

    if request.form:
        cleaned_date = datetime.datetime.strptime(
            request.form['date'], '%Y-%m'
        )

        new_project = Project(
            title=request.form['title'],
            date=cleaned_date,
            description=request.form['desc'],
            skills_practiced=request.form['skills'],
            url=request.form['github']
        )

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('new_project.html', projects=projects)


@app.route('/projects/<int:id>')
def detail(id):
    projects = db.session.query(Project).all()
    project = db.one_or_404(db.select(Project).filter_by(id=id))

    return render_template(
        'detail.html',
        project=project,
        id=id,
        skills=project.skills_practiced,
        projects=projects
    )


@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if not check_auth():
        return authenticate()

    projects = db.session.query(Project).all()
    project = db.one_or_404(db.select(Project).filter_by(id=id))

    if request.method == 'POST':
        project.title = request.form['title']
        project.date = datetime.datetime.strptime(
            request.form['date'], '%Y-%m'
        )
        project.description = request.form['desc']
        project.skills_practiced = request.form['skills']
        project.url = request.form['github']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template(
        'edit_project.html',
        project=project,
        projects=projects,
        id=project.id,
        date=datetime.datetime.strftime(project.date.date(), '%Y-%m')
    )


@app.route('/projects/<int:id>/delete')
def delete(id):
    if not check_auth():
        return authenticate()

    project = db.one_or_404(db.select(Project).filter_by(id=id))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    projects = db.session.query(Project).all()
    return render_template('about.html', projects=projects)


# ------------------------
# ERROR HANDLER
# ------------------------
@app.errorhandler(404)
def not_found(error):
    projects = db.session.query(Project).all()
    return render_template('404.html', projects=projects), 404


# ------------------------
# RUN APP
# ------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(port=3000, debug=True, host='0.0.0.0')

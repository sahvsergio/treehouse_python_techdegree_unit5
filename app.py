# --- Core Flask & DB ---
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify, Response
from models import Project, app, db

# --- Auth ---
from flask_basicauth import BasicAuth

# --- Flask-Admin ---
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# --- Utilities ---
import datetime
from io import StringIO
import csv

# ------------------------
# BASIC AUTH CONFIG
# ------------------------
app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
basic_auth = BasicAuth(app)

# ------------------------
# PROTECT ADMIN INDEX
# ------------------------
class MyAdminIndexView(AdminIndexView):
    def dispatch_request(self):
        if not basic_auth.authenticate():
            return Response(
                'Login required',
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        return super().dispatch_request()

# ------------------------
# ADMIN SETUP
# ------------------------
app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'

admin = Admin(
    app,
    name='My portfolio',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView()
)

class ProjectView(ModelView):
    def is_accessible(self):
        return basic_auth.authenticate()

    def inaccessible_callback(self, name, **kwargs):
        return abort(401)

admin.add_view(ProjectView(Project, db.session))

# ------------------------
# ROUTES
# ------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    projects = db.session.query(Project).all()
    return render_template('index.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
@basic_auth.required
def create():
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
@basic_auth.required
def edit(id):
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
@basic_auth.required
def delete(id):
    project = db.one_or_404(db.select(Project).filter_by(id=id))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    projects = db.session.query(Project).all()
    return render_template('about.html', projects=projects)


# ------------------------
# BACKUP (CSV DOWNLOAD)
# ------------------------
@app.route('/backup')
@basic_auth.required
def backup():
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'id', 'title', 'date', 'description', 'skills', 'url'
    ])

    projects = db.session.query(Project).all()

    for p in projects:
        writer.writerow([
            p.id,
            p.title,
            p.date,
            p.description,
            p.skills_practiced,
            p.url
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=projects_backup.csv"
        }
    )


# ------------------------
# IMPORT CSV
# ------------------------
@app.route('/import', methods=['POST'])
@basic_auth.required
def import_csv():
    file = request.files['file']

    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_data = csv.DictReader(stream)

    for row in csv_data:
        existing = db.session.query(Project).filter_by(
            title=row['title']
        ).first()

        if not existing:
            new_project = Project(
                title=row['title'],
                date=datetime.datetime.strptime(row['date'], '%Y-%m'),
                description=row['description'],
                skills_practiced=row['skills'],
                url=row['url']
            )
            db.session.add(new_project)

    db.session.commit()

    return redirect(url_for('index'))


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

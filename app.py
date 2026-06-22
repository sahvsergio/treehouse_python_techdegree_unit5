# ------------------------
# CORE IMPORTS
# ------------------------
import html
from flask import (
    abort, redirect, render_template,
    request, url_for, Response
)
from req import (
    get_treehouse_data,
    extract_wordpress_blog,
    extract_blogger_sahvsergio,
    extract_blogger_unana,
    extract_blogger_gepido
)

from models import Project, app, db

# ------------------------
# ADMIN
# ------------------------
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# ------------------------
# UTILITIES
# ------------------------
import datetime
from io import StringIO
import csv








app.config['FLASK_ADMIN_SWATCH'] = 'simplex'
admin = Admin(app)








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


@app.route('/init-db')
def init_db():
    with app.app_context():
        db.create_all()
    return "DB initialized"

@app.route('/blogs')
def show_blogs():
    print("🚀 Flask route triggered: Fetching live streams into memory...")
    
    wp_posts = extract_wordpress_blog()
    b1_posts = extract_blogger_sahvsergio()
    b2_posts = extract_blogger_unana()
    b3_posts = extract_blogger_gepido()
    
    all_current_posts = wp_posts + b1_posts + b2_posts + b3_posts
    treehouse_profile = get_treehouse_data()
    
    # Clean up every single text entity (like &nbsp;) inside your post dictionaries
    cleaned_posts = []
    for post in all_current_posts:
        cleaned_post = {
            'title': html.unescape(post.get('title', '')),
            'url': post.get('url', ''),
            'source': post.get('source', ''),
            'description': html.unescape(post.get('description', ''))
        }
        cleaned_posts.append(cleaned_post)
    
    return render_template(
        'blogs.html', 
        posts=cleaned_posts,  # Pass the cleaned array
        profile=treehouse_profile

    )
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

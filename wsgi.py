from models import app, db  # Import from models.py, since app and db are defined there

# Ensure the database is set up
with app.app_context():
    db.create_all()

# The WSGI server will use this app object
if __name__ == "__main__":
    app.run()

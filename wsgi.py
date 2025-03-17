from models import app, db

if __name__ == '__main__':
    with app.app_context():
        # creating the engine
        engine = db.engine
        db.create_all()

    # making the app run, you just need to run the app.py file on the terminal
    # local app.run(debug=True , port=8000, host='127.0.0.1')
     # internet
    app.run( port=8000, debug=True, host='127.0.0.1')
from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from location.models import db

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile("config.py", silent=True)
    db.init_app(app)
    migrate = Migrate(app,db)
    socketio = SocketIO(app)
    csrf.init_app(app)
    return app, socketio
app, socketio = create_app()




from location import user_routes
from location.forms import *







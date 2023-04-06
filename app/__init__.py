from flask import Flask
from flask_bootstrap5 import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

app = Flask(__name__)
bootstrap = Bootstrap()
bootstrap.init_app(app)
app.config.from_object(Config)
socketio = SocketIO(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

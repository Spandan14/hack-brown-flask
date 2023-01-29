from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# this creates an instance of the Flask class, and __name__ is a
# predefined variable which is the name of the module (app)
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# we include this import at the end because routes needs to import
# the app object first, then we can import routes inside app
# this prevents a circular import
from app import routes, models
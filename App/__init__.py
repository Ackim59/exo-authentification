from flask import Flask
from dotenv import load_dotenv
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_authorize import Authorize

load_dotenv(override=True)

db = SQLAlchemy()
authorize = Authorize()

config_name = "development"

app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Démarrage du monitoring
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=' + os.environ.get("CONNECTION_STRING")))
logger.setLevel(logging.WARN)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# authorize = Authorize(app)
# Connect sqlalchemy to app
db.init_app(app)

@app.cli.command("init_db")
def init_db():
    from App import models
    models.init_db()

# blueprint for auth routes in our app
from App.views.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
# from App.views.auth import google as google_blueprint
# app.register_blueprint(google_blueprint, url_prefix="/google_login")

# blueprint for non-auth parts of app
from App.views.main import main as main_blueprint
app.register_blueprint(main_blueprint)
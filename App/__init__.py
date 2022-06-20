from flask import Flask, render_template
from .views import app
from . import model

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .model import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Connect sqlalchemy to app
model.db.init_app(app)

@app.cli.command("init_db")
def init_db():
    model.init_db()
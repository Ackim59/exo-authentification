from flask import Flask, render_template, url_for, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from dotenv import load_dotenv
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from .model import User, db

# Démarrage du monitoring
load_dotenv()
APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
# logger = logging.getLogger(__name__)
# logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=393a5c37-b4b6-47e6-87db-2012a7af0e1b'))

# for i in range(15):
# logger.warning("hello world!")


@app.route("/")
@app.route("/index/")
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('board_page'))

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))

@app.route('/board')
@login_required
def board_page():
    return render_template('board.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
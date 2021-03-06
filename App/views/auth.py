from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.google import make_google_blueprint, google
from App.models import User, Role
from App.models import db
from App.forms import Login, Signup
import random, string
import os

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# google authentication

google_blueprint = make_google_blueprint(client_id = os.getenv('GOOGLE_CLIENT_ID'),
                                         client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
                                         reprompt_consent = True,
                                         scope = ["profile", "email"],
                                         redirect_to = "auth.login"
                                         )
                                        

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """[Allow to ask login and generate the template of login.html on login path]

    Returns:
        [str]: [login page code]
    """
    if (not current_user.is_authenticated) & (google.token is None):
        form = Login()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Vous êtes connecté en tant que : {user.name} {user.email}",category="success")
                return redirect(url_for('main.board'))
            else:
                flash('Adresse email ou mot de passe invalide',category="danger")
        return render_template('login.html',form=form)
    elif (not current_user.is_authenticated) & (google.token is not None):
        user_info_endpoint = "oauth2/v2/userinfo"
        google_data = google.get(user_info_endpoint).json()
        user = User.query.filter_by(email=google_data['email']).first()
        flash(f"Vous êtes connecté en tant que : {google_data['name']} {google_data['email']}",category="success")
        # If user exists go to board page else add user in database and go to board page
        if user:
            login_user(user)
            return redirect(url_for('main.board'))
        else:
            # To generate a new secret key:
            password = "".join([random.choice(string.printable) for _ in range(24)])
            password = generate_password_hash(password, method='sha256')
            # add the user in the database
            User.create_user(google_data['name'], password, google_data['email'])
            # get the user from database and save in session
            user = User.query.filter_by(email=google_data['email']).first()
            login_user(user)
            return redirect(url_for('main.board'))
    else:
        return redirect(url_for('main.board'))

@auth.route("/google_login")
def google_login():
    return redirect(url_for('google.login'))

@auth.route('/signup')
def signup():
    form = Signup()
    return render_template('signup.html', form=form)

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    form = Signup()
    if form.validate_on_submit():
        
        email = form.email.data
        name = form.name.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        elif password != confirm_password:
            flash("Passwords don't match")
            return redirect(url_for('auth.signup'))
        else:
            User.create_user(name, password, email)
            flash("You successfully subscribe")
            return redirect(url_for('auth.login')) 

@auth.route('/logout')
def logout():
    if google_blueprint.token is not None:
        token = google_blueprint.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert resp.ok, resp.text
        del google_blueprint.token  # Delete OAuth token from storage
    if current_user.is_authenticated:
        logout_user()        # Delete Flask-Login's session cookie

    return redirect(url_for('main.home'))

from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.google import make_google_blueprint, google
from App.models import User, Role
from App import db, app
import os

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# google authentication
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

google_blueprint = make_google_blueprint(client_id = os.getenv('GOOGLE_CLIENT_ID'),
                                         client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
                                         reprompt_consent = True,
                                         scope = ["profile", "email"],
                                         redirect_to = "main.board_page"
                                         )
app.register_blueprint(google_blueprint, url_prefix="/google_login")

@auth.route('/login_page')
def login_page():

    return render_template('login.html')

@auth.route('/login')
def login():

        if google_blueprint.token is None:
            return render_template("classic_login.html")
        else:
            google_data = None
            user_info_endpoint = "oauth2/v2/userinfo"
            if google.authorized:
                google_data = google.get(user_info_endpoint).json()
            return render_template('board.html', google_data=google_data, fetch_url=google.base_url + user_info_endpoint)


# @auth.route('/login', methods=['POST'])
# def login():
    
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False

#     user = User.query.filter_by(email=email).first()
#     # check if the user actually exists
#     # take the user-supplied password, hash it, and compare it to the hashed password in the database
#     if not user or not check_password_hash(user.password, password):
#         return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
#     # if the above check passes, then we know the user has the right credentials
#     login_user(user, remember=remember)
#     return redirect(url_for('main.board_page'))
#     # return redirect(url_for('main.board_page'))
#     # if user.roles == 'User':
#     #     return redirect(url_for('main.board_page'))
#     # elif user.roles == 'Admin':
#     #     return redirect(url_for('main.admin_board_page'))

@auth.route("/google_login")
def google_login():
    return redirect(url_for('google.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

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
    elif current_user.is_authenticated:
        logout_user()        # Delete Flask-Login's session cookie

    return redirect(url_for('main.home'))

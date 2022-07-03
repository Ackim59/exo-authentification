from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, login_required, current_user, logout_user
from flask_security import roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.google import google
from App.models import User

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")

@main.route("/")
@main.route("/index/")
def home():
    return render_template('index.html')


@main.route('/board')
# @authorize.has_role('User')
@login_required
def board():

    if google.token is None:
        import logging
        logging.warning("coucou")
        name = current_user.name
        email = current_user.email
        login_google = False

    else:
        import logging
        logging.warning("authentifié ?" + str(current_user.is_authenticated))
        user_info_endpoint = "oauth2/v2/userinfo"
        google_data = google.get(user_info_endpoint).json()
        name = google_data['name']
        email = google_data['email']
        login_google = True
    return render_template('board.html', name=name, email=email, login_google=login_google)#, name=current_user.name)

@main.route('/admin_board')
def admin_board():
    return render_template('admin_board.html', name=current_user.name)
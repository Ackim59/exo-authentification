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
    if current_user.is_authenticated:
        name = current_user.name
    elif google.token is not None:
        name = google.name
    user_info_endpoint = "oauth2/v2/userinfo"
    import logging
    logging.warning(google.get(user_info_endpoint).json())
    return name#render_template('board.html')#, name=current_user.name)

@main.route('/admin_board')
def admin_board():
    return render_template('admin_board.html', name=current_user.name)
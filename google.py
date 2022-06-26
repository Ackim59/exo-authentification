import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import logging

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

google_blueprint = make_google_blueprint(client_id = os.getenv('GOOGLE_CLIENT_ID'),
                                         client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
                                         reprompt_consent = True,
                                         scope = ["profile", "email"]
                                         )
app.register_blueprint(google_blueprint, url_prefix="/google_login")

@app.route("/")
def index_test():
    google_data = None
    user_info_endpoint = "oauth2/v2/userinfo"
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
    
    return render_template('index_test.html', google_data=google_data, fetch_url=google.base_url + user_info_endpoint)

@app.route("/google_login")
def google_login():
    return redirect(url_for('google.login'))

@app.route("/google_logout")
def google_logout():
    token = google_blueprint.token["access_token"]
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.ok, resp.text
    # logout_user()        # Delete Flask-Login's session cookie
    del google_blueprint.token  # Delete OAuth token from storage
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

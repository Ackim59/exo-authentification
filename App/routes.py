from flask import render_template
from App import app

@app.route("/")
@app.route("/index/")
def home():
    return render_template(("index.html"))
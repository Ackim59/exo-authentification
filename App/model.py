from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

from .views import app

# Create database connection object
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)

import logging as lg

def init_db():
    db.drop_all()
    db.create_all()
    for i in range(5):
        db.session.add(User(
                            email = 'toto' + str(i) + '@' + 'exemple.com',
                            name = "toto" + str(i),
                            password = generate_password_hash("1234", method='sha256')
                            ))
    db.session.commit()
    lg.warning('Database initialized!')
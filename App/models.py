from werkzeug.security import generate_password_hash
from flask_authorize import RestrictionsMixin
from flask_login import UserMixin
import logging as lg
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_roles = db.Table('user_roles', db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    roles = db.relationship('Role', secondary=user_roles)

    @classmethod
    def create_user(self, name, password, email):
        import logging
        logging.warning("en cours denregistrement -----------------------------------------------------------------")
        user = User(
                    email = email,
                    name = name,
                    password = generate_password_hash(password, method='sha256')
                    )
        db.session.add(user)
        db.session.commit()

class Role(db.Model):#, RestrictionsMixin
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

def init_db():
    db.drop_all()
    db.create_all()
    # admin_role = Role(name='Admin')
    user_role = Role(name='User')
    for i in range(2):
        user = User(
                    email = 'toto' + str(i+1) + '@' + 'exemple.com',
                    name = "toto" + str(i+1),
                    password = generate_password_hash("1234", method='sha256')
                    )
        user.roles.append(user_role)
        db.session.add(user)
    db.session.commit()
    # user = User(
    #             email = 'tata@exemple.com',
    #             name = 'tata',
    #             password = generate_password_hash("1234", method='sha256')
    #             )
    # user.roles.append(admin_role)
    # db.session.add(user)
    # db.session.commit()
    lg.warning('Database initialized!')
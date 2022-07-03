from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField, StringField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")

class Signup(FlaskForm):
    """[Form to signup]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    name = StringField(label="Nom:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    confirm_password = PasswordField(label="Confirmer le mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="S'enregistrer")
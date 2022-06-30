from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from app.models import User

class PackageRegistrationForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired()])
    cod = StringField('Código de Rastreio', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Encomenda')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    rememberMe = BooleanField('Lembre-me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Digite a Senha', validators=[DataRequired()])
    password2 = PasswordField('Repita a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

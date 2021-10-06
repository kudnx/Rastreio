from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PackageRegistrationForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired()])
    cod = StringField('Código de Rastreio', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Encomenda')
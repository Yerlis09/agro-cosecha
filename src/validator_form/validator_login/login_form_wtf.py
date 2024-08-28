from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Correo electronico', validators=[DataRequired(), Length(min=10, max=35)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Iniciar sesión')
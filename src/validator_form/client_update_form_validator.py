from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,  SubmitField, SelectField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional

class ClienteUpdateForm(FlaskForm):
    tipo_identificacion = SelectField('Tipo documento', choices=[
    ('', 'Seleccione'),
    ('CC', 'Cédula de Ciudadanía'),
    ('NIT', 'NIT')], validators=[DataRequired()])
    nombres = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    departamento = SelectField('Departamento', choices=[], validators=[DataRequired()])
    municipio = SelectField('Municipio', choices=[], validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    identificacion = StringField('Identificación', validators=[DataRequired()])
    experiencia = StringField('Experiencia', validators=[DataRequired()])
    estudios_realizados = StringField('Estudios Realizados', validators=[DataRequired()])
    correo = EmailField('Correo', validators=[DataRequired(), Email()])
    clave = PasswordField('Clave', validators=[Optional(), Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')])
    rol = SelectField('Rol', choices=[
    ('', 'Seleccione'),
    ('R-A1', 'Administrador'),
    ('R-AG2', 'Agronomo'),
    ('R-R3', 'Responsable'),
    ('R-AGR4', 'Agricultor'),
    ('R-O5', 'Otro')], validators=[DataRequired()])
    celular = StringField('Celular', validators=[DataRequired()])
    submit1 = SubmitField('Guardar')
    submit2 = SubmitField('Guardar')



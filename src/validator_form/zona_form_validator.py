from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ZonaForm(FlaskForm):
    nombre_zona = StringField('Nombre de zona', validators=[DataRequired()])
    area_cultivada = StringField('Área cultivada', validators=[DataRequired()])
    especie = StringField('Especie', validators=[DataRequired()])
    variedad = StringField('Variedad', validators=[DataRequired()])
    tratamiento = SelectField('Tratamiento', choices=[
    ('', 'Seleccione'),
    ('A1', 'Arado mecanizado'),
    ('H2', 'Hidratación manual'),
    ('F3', 'Fertilización')], validators=[DataRequired()])
    secano_regio = SelectField('Secano/regio', choices=[
    ('', 'Seleccione'),
    ('S1', 'Secano'),
    ('A2', 'Aspersión'),
    ('G3', 'Goteo o localizado'),
    ('P4', 'Por gravedad'),
    ('L5', 'Lluvia')
    ], validators=[DataRequired()])
    proteccion_cult = SelectField('Protección cultivo', choices=[
    ('', 'Seleccione'),
    ('A1', 'Aire libre'),
    ('M2', 'Malla'),
    ('C3', 'Cubierta bajo plástico'),
    ('I4', 'Invernadero')
    ], validators=[DataRequired()])
    captac_agua = StringField('Captación del agua', validators=[DataRequired()])
    descripcion_zona = TextAreaField('Descripción zona', validators=[DataRequired()])
    n_puntos = IntegerField('# de puntos', validators=[DataRequired()])
    ubicacion = StringField('Coordenadas del Polígono', validators=[DataRequired()])
    submit = SubmitField('Guardar')
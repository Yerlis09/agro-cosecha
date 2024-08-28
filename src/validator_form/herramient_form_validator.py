from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class HerramientaForm(FlaskForm):
    nombre_equipo = StringField('Nombre de equipo', validators=[DataRequired()])
    funcionalidad_equipo = StringField('Funcionalidad del equipo', validators=[DataRequired()])
    fecha_inicio_uti = DateField('Fecha inicio de utilización del equipo', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_fin_uti = DateField('Fecha fin de utilización del equipo', format='%Y-%m-%d', validators=[DataRequired()])
    activo = BooleanField('Activo')
    submit = SubmitField('Guardar')

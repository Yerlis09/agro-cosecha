from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

class SensorForm(FlaskForm):
    sensor = StringField('Sensor', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    hora_inicio = TimeField('Hora de inicio', format='%H:%M', validators=[DataRequired()])
    hora_fin = TimeField('Hora de fin', format='%H:%M', validators=[DataRequired()])
    observ = TextAreaField('Observación', validators=[DataRequired()])
    listLayerId = HiddenField('listLayerId', validators=[DataRequired()])
    listOutLayerId = HiddenField('listOutLayerId', validators=[DataRequired()])
    submit1 = SubmitField('Guardar')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, HiddenField, TextAreaField
from wtforms.validators import DataRequired

class InspeccionForm(FlaskForm):
    inspeccion = StringField('Inspección', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    hora_inicio = TimeField('Hora de inicio', validators=[DataRequired()])
    hora_fin = TimeField('Hora de fin', validators=[DataRequired()])
    observ = TextAreaField('Observación', validators=[DataRequired()])
    listLayerId = HiddenField('ListLayerId', validators=[DataRequired()])
    listOutLayerId = HiddenField('ListOutLayerId', validators=[DataRequired()])
    submit = SubmitField('Guardar')

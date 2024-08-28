from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ParcelaForm(FlaskForm):
    nombre_parcela = StringField('Nombre de Parcela', validators=[DataRequired()])
    n_hileras = IntegerField('Número de hileras', validators=[DataRequired()])
    separacion_hilera = StringField('Separación entre hileras', validators=[DataRequired()])
    separacion_planta = StringField('Separación entre plantas', validators=[DataRequired()])
    n_plantas = StringField('Número de plantas', validators=[DataRequired()])
    coordP = StringField('Úbicación de la parcela', validators=[DataRequired()])
    submit = SubmitField('Guardar')

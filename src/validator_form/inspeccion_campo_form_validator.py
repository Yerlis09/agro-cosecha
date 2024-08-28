from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, SelectField
from wtforms.validators import DataRequired

class InspeccionCampoForm(FlaskForm):
    nombre = StringField('Nombre de la inspección', validators=[DataRequired()])
    fecha = DateField('Fecha de inspección', format='%Y-%m-%d', validators=[DataRequired()])
    dat_bitacora = StringField('Bitácora', validators=[DataRequired()])
    id_cuaderno = HiddenField('Id cuaderno', validators=[DataRequired()])
    submit = SubmitField('Guardar')

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class BitacoraForm(FlaskForm):
    nombre_bitacora = StringField('Nombre de bitacora', validators=[DataRequired()])
    fecha_apertura = DateField('Fecha de apertura del cuaderno', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de inicio del cultivo', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de fin del cultivo', validators=[DataRequired()])
    tipo_cultivo = SelectField('Seleccione tipo de cultivo', choices=[
    ('', 'Seleccione'),
    ('E1', 'Estacionario'),
    ('R2', 'Rotativo')], validators=[DataRequired()])
    nombre_encargado = StringField('Nombre del encargado', validators=[DataRequired()])
    nro_ident_enc = StringField("Número de identificación", validators=[DataRequired()])
    personas_json = HiddenField('Personas que intervienen', validators=[DataRequired()])
    equipos_json = HiddenField('Herramientas', validators=[DataRequired()])
    nombre_zona = HiddenField('Nombre zona', validators=[DataRequired()])
    coordenadas_zona = HiddenField('Coordenadas de la zona', validators=[DataRequired()])
    id_zona = HiddenField('Id de la zona', validators=[DataRequired()])
    lista_parcelas = HiddenField('Lista de parcelas', validators=[DataRequired()])
    submit = SubmitField('Guardar')

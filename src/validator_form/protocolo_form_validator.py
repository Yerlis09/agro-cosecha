from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, HiddenField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class ProtocoloForm(FlaskForm):
    dat_bitacora = StringField('Bitácora', validators=[DataRequired()])
    id_cuaderno = HiddenField('Id cuaderno', validators=[DataRequired()])
    fecha_inicio_pres = DateField('Fecha inicio prescripción', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_fin_pres = DateField('Fecha fin prescripción', format='%Y-%m-%d', validators=[DataRequired()])
    nombre_pres = StringField('Nombre prescripción', validators=[DataRequired()])
    alt_no_quimica = SelectField('Seleccione', choices=[
    ('', 'Seleccione'),
    ('A1', 'Aplica'),
    ('N2', 'No aplica')], validators=[DataRequired()])
    descr_alt_no_quimica = TextAreaField("Escriba la aplicacion de alternativa no quimica")
    detec_plaga = SelectField('Seleccione', choices=[
    ('', 'Seleccione'),
    ('S1', 'Si'),
    ('N2', 'No')], validators=[DataRequired()]) 
    #OBSERVACIÓN: Aplicación de alternativa quimica seria lo mismo que Aplicación de alternativa no quimica
    hidrat_cultivo = SelectField('Seleccione', choices=[
    ('', 'Seleccione'),
    ('N1', 'Normal'),
    ('N2', 'No aplica')], validators=[DataRequired()]) 
    nutren_suelo = SelectField('Seleccione', choices=[
    ('', 'Seleccione'),
    ('A1', 'Alto'),
    ('B2', 'Bajo')], validators=[DataRequired()]) 
    dosis_util = SelectField('Seleccione', choices=[
    ('', 'Seleccione'),
    ('N1', 'Normal'),
    ('N2', 'No aplica')], validators=[DataRequired()]) 
    infor_obt_desde = SelectField('Seleccione', choices=[
    ('', 'Seleccione'),
    ('V1', 'Vuelos'),
    ('D2', 'Detectores'),
    ('I3', 'Inspecciones de campo')], validators=[DataRequired()])
    list_detect_select = HiddenField('Lista detectores seleccionados')
    list_vuelo_select = HiddenField('Lista vuelos seleccionados')
    list_insp_select =  HiddenField('Lista inspecciones seleccionados')
    list_herra_select = HiddenField('Lista herramientas seleccionados', validators=[DataRequired()])
    submit1 = SubmitField('Guardar')


from flask import render_template, url_for, flash, session
from werkzeug.utils import redirect

from . import herramienta_bp
from src.services.herramienta_service.herramienta_service import Herramienta_service
from src.validator_form.herramient_form_validator import HerramientaForm


@herramienta_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = HerramientaForm()

    if form.validate_on_submit():
        try:
            herramienta = get_herramienta_dic_from(form)

            print("Herramienta creada:", herramienta) 
            
            Herramienta_service.agregar_nueva_herramienta(herramienta)
            return redirect(url_for('herramienta_route.mostrar_herramientas'))
        except ValueError as e:
            flash(str(e))
            return render_template('/herramienta/herramienta_form.html', form=form)
        except Exception as e:
            flash(f"Error al guardar los datos: {e}")
            return render_template('/herramienta/herramienta_form.html', form=form)
    else:
        print(form.errors)
    return render_template('/herramienta/herramienta_form.html', form=form)


@herramienta_bp.route('/mostrar_registros_herramientas', methods=['GET', 'POST'])
def mostrar_herramientas():
    form = HerramientaForm()

    try:
        herramientas = Herramienta_service.obtener_registros_herramientas()
    except Exception as e:
        flash(f"Error al obtener los herramientas: {e}", "danger")
        herramientas = []
    return render_template('/herramienta/herramienta_form.html', form=form, herramientas=herramientas)


@herramienta_bp.route('/update/<id>', methods=['POST'])
def postUpdate(id):
    form = HerramientaForm()    
    datosUpdate = get_herramienta_dic_from(form)

    if not datosUpdate:
        flash("Herramienta no encontrado", "warning")

    if form.validate_on_submit():
        try:
            Herramienta_service.modificar_una_herramienta(id, datosUpdate)
            flash('Herramienta actualizado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al actualizar herramienta: {e}', 'danger')
    else:
        print(form.errors)
        flash('Error en el formulario', "danger")
    
    return redirect(url_for('herramienta_route.mostrar_herramientas'))


@herramienta_bp.route('/delete/<id>', methods=['POST'])
def delete_herramienta(id):
    try:
        Herramienta_service.eliminar_herramienta(id)
        print('Herramienta eliminado exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar herramienta: {e}', 'danger')
    return redirect(url_for('herramienta_route.mostrar_herramientas'))


def get_herramienta_dic_from(form):

    # Verifica si algún campo obligatorio está vacío
    if not form.nombre_equipo.data:
        raise ValueError("El campo 'tipo identificacion' no puede estar vacío")
    if not form.funcionalidad_equipo.data:
        raise ValueError("El campo 'funcionalidad_equipo' no puede estar vacío")
    if not form.fecha_inicio_uti.data:
        raise ValueError("El campo 'fecha_inicio_uti' no puede estar vacío")
    if not form.fecha_fin_uti.data:
        raise ValueError("El campo 'fecha_fin_uti' no puede estar vacío")
    
    return {
        'nombre_equipo': form.nombre_equipo.data,
        'funcionalidad_equipo': form.funcionalidad_equipo.data,
        'fecha_inicio_uti': form.fecha_inicio_uti.data,
        'fecha_fin_uti': form.fecha_fin_uti.data,
        'activo': form.activo.data or False
    }

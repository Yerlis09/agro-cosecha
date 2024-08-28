from flask import render_template, url_for, flash
from flask.json import jsonify
import requests
from werkzeug.utils import redirect

from . import zona_bp
from src.services.zona_service.zona_service import ZonaService
from src.validator_form.zona_form_validator import ZonaForm
from src.validator_form.parcela_form_wtf import ParcelaForm


@zona_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = ZonaForm()

    if form.validate_on_submit():
        try:
            zona = get_zona_dic_from(form)
            print("entre 2")
            print("Zona creada:", zona) 
            
            ZonaService.agregar_nuevo_zona(zona)
            return jsonify({'success': True}), 200
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': f"Error al guardar los datos: {e}"}), 500
    else:
        # Devuelve los errores del formulario como JSON y renderiza la vista con el formulario
        errors = form.errors
        print("Errores del formulario:", errors)
        return render_template('/zonas_parcelas/add_zona_form.html', form=form), 400

@zona_bp.route('/mostrar_registros_zona', methods=['GET', 'POST'])
def mostrar_zona():
    form = ZonaForm()

    try:
        zonas = ZonaService.obtener_registros_zonas()
    except Exception as e:
        print("Error al obtener los zonas")
        zonas = []
    return render_template('/zonas_parcelas/zona_form.html', form=form, zonas=zonas)


@zona_bp.route('/update/<id>', methods=['POST'])
def postUpdate(id):
    form = ZonaForm()    
    datosUpdate = get_zona_dic_from(form)

    if not datosUpdate:
        print("Zona no encontrado", "warning")

    if form.validate_on_submit():
        try:
            ZonaService.modificar_una_zona(id, datosUpdate)
            flash('Zona actualizado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al actualizar zona: {e}', 'danger')
    else:
        print(form.errors)
        flash('Error en el formulario', "danger")
    
    return redirect(url_for('zona_route.mostrar_zona'))


@zona_bp.route('/delete/<id>', methods=['POST'])
def delete_zona(id):
    try:
        ZonaService.eliminar_zona(id)
        print('Zona eliminada exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar zona: {e}', 'danger')
    return redirect(url_for('zona_route.mostrar_zona'))


@zona_bp.route('/ver/<id>', methods=['GET'])
def ver_zona(id):
    print("Prueba 1")
    form = ParcelaForm()
    try:
        print("Prueba 2")
        zona = ZonaService.obtener_zona_por_id(id)
        print("Prueba 3")
        print(zona)
        if not zona:
            flash('Zona no encontrada', 'danger')
            return redirect(url_for('zona_route.mostrar_zona'))

        return render_template('/zonas_parcelas/ver_zona.html', zona=zona, form=form)
    except Exception as e:
        flash(f'Error al cargar la zona: {e}', 'danger')
        return redirect(url_for('zona_route.mostrar_zona'))
    
    
@zona_bp.route('/agregar_parcela/<id>', methods=['POST'])
def agregar_parcela(id):
    form = ParcelaForm()
    if form.validate_on_submit():
        try:
            parcela = {
                'nombre_parcela': form.nombre_parcela.data,
                'n_hileras': form.n_hileras.data,
                'separacion_hilera': form.separacion_hilera.data,
                'separacion_planta': form.separacion_planta.data,
                'n_plantas': form.n_plantas.data,
                'coordP': form.coordP.data
            }
            
            ZonaService.agregar_parcela_a_zona(id, parcela)
            return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': f"Error al guardar los datos: {e}"}), 500
    else:
        print(form.errors)
        return jsonify({'success': False, 'error': form.errors}), 400

def get_zona_dic_from(form):
    # Verifica si algún campo obligatorio está vacío
    if not form.nombre_zona.data:
        raise ValueError("El campo 'nombre zona' no puede estar vacío")
    if not form.area_cultivada.data:
        raise ValueError("El campo 'area cultivada' no puede estar vacío")
    if not form.especie.data:
        raise ValueError("El campo 'especie' no puede estar vacío")
    if not form.variedad.data:
        raise ValueError("El campo 'variedad' no puede estar vacío")
    if not form.tratamiento.data:
        raise ValueError("El campo 'tratamiento' no puede estar vacío")
    if not form.secano_regio.data:
        raise ValueError("El campo 'secano/regio' no puede estar vacío")
    if not form.proteccion_cult.data:
        raise ValueError("El campo 'protección cultivo' no puede estar vacío")
    if not form.captac_agua.data:
        raise ValueError("El campo 'captación agua' no puede estar vacío")
    if not form.descripcion_zona.data:
        raise ValueError("El campo 'descripción zona' no puede estar vacío")
    if not form.n_puntos.data:
        raise ValueError("El campo '# de puntos' no puede estar vacío")
    if not form.ubicacion.data:
        raise ValueError("El campo 'ubicación' no puede estar vacío")
    
    return {
        'nombre_zona': form.nombre_zona.data,
        'area_cultivada': form.area_cultivada.data,
        'especie': form.especie.data,
        'variedad': form.variedad.data,
        'tratamiento': form.tratamiento.data,
        'secano_regio': form.secano_regio.data,
        'proteccion_cult': form.proteccion_cult.data,
        'captac_agua': form.captac_agua.data,
        'descripcion_zona': form.descripcion_zona.data,
        'n_puntos': form.n_puntos.data,
        'ubicacion': form.ubicacion.data
    }
from flask import render_template, url_for, flash, request, jsonify
from werkzeug.utils import redirect
import json
from datetime import datetime

from . import inspeccion_campo_bp
from src.services.inspeccion_campo_service.inspeccion_campo_service import InspeccionCampoService
from src.services.bitacora_service.bitacora_service import Bitacora_service
from src.validator_form.inspeccion_campo_form_validator import InspeccionCampoForm
from src.validator_form.inspeccion_form_validator import InspeccionForm


@inspeccion_campo_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = InspeccionCampoForm()

    if form.validate_on_submit():
        try:
            inspeccion_campo = get_inspeccion_campo_dic_from(form)
            
            InspeccionCampoService.agregar_nueva_inspeccion_campo(inspeccion_campo)
            return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))
        except ValueError as e:
            flash(str(e))
            return render_template('/inspeccion_campo/add_inspeccion_form.html', form=form)
        except Exception as e:
            flash(f"Error al guardar los datos: {e}")
            return render_template('/inspeccion_campo/add_inspeccion_form.html', form=form)
    else:
        print(form.errors)
    return render_template('/inspeccion_campo/add_inspeccion_form.html', form=form)


@inspeccion_campo_bp.route('/mostrar_registros_inspecciones_campo', methods=['GET', 'POST'])
def mostrar_inspecciones_campo():
    form = InspeccionCampoForm()

    try:
        inspecciones_campo = InspeccionCampoService.obtener_registros_inspecciones_campo()

         # Validar y setear 'inspecciones_realizadas'
        for inspeccion_campo in inspecciones_campo:
            # Convertir nombre_bitacora a cadena si es una tupla
            if isinstance(inspeccion_campo.nombre_bitacora, tuple):
                print("entre al if de conversion de tupla a string de nombre_bitacora")
                try:
                    inspeccion_campo.nombre_bitacora = str(inspeccion_campo.nombre_bitacora[0])
                except (ValueError, IndexError) as e:
                    print(f"Error al convertir nombre_bitacora de tupla a string: {inspeccion_campo.nombre_bitacora}, Error: {e}")
                    inspeccion_campo.nombre_bitacora = ""  # Valor predeterminado en caso de error

    except Exception as e:
        flash(f"Error al obtener las inspecciones de campo: {e}", "danger")
        inspecciones_campo = []
    return render_template('/inspeccion_campo/inspeccion_campo_form.html', form=form, inspecciones_campo=inspecciones_campo)


@inspeccion_campo_bp.route('/mostrar_inspeccion_campo/<id>', methods=['GET', 'POST'])
def mostrar_inspeccion_campo(id):
    form = InspeccionCampoForm()
    inspeccion_form = InspeccionForm()
    try:
        inspeccion_campo = InspeccionCampoService.obtener_inspeccion_campo_por_id(id)
        if not inspeccion_campo:
            flash('Inspección de campo no encontrada', 'danger')
            return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))

        # Convertir la fecha de str a datetime.date
        if isinstance(inspeccion_campo['fecha'], str):
            inspeccion_campo['fecha'] = datetime.strptime(inspeccion_campo['fecha'], '%Y-%m-%d').date()


        # Prellenar el formulario con los datos de la inspección de campo
        form.nombre.data = inspeccion_campo['nombre']
        form.fecha.data = inspeccion_campo['fecha']
        form.dat_bitacora.data = inspeccion_campo['nombre_bitacora']
        form.id_cuaderno.data = inspeccion_campo['id_bitacora']

        return render_template('/inspeccion_campo/update_inspeccion_campo.html', form=form, inspeccion_campo=inspeccion_campo, inspeccion_form=inspeccion_form)
    except Exception as e:
        flash(f'Error al cargar la inspección de campo: {e}', 'danger')
        return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))


@inspeccion_campo_bp.route('/delete/<id>', methods=['POST'])
def delete_inspeccion_campo(id):
    try:
        InspeccionCampoService.eliminar_inspeccion_campo(id)
        print('Inspección de campo eliminada exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar inspección de campo: {e}', 'danger')
    return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))


def get_inspeccion_campo_dic_from(form):
    # Verifica si algún campo obligatorio está vacío
    if not form.nombre.data:
        raise ValueError("El campo 'nombre de la inspección' no puede estar vacío")
    if not form.fecha.data:
        raise ValueError("El campo 'fecha de la inspección' no puede estar vacío")
    if not form.dat_bitacora.data:
        raise ValueError("El campo 'nombre de bitácora' no puede estar vacío")
    if not form.id_cuaderno.data:
        raise ValueError("El campo 'id_cuaderno' no puede estar vacío")
    
    return {
        'nombre': form.nombre.data,
        'fecha': form.fecha.data,
        'nombre_bitacora': form.dat_bitacora.data,
        'id_bitacora': form.id_cuaderno.data,
    }


@inspeccion_campo_bp.route('/filtrar_bitacoras', methods=['POST'])
def filtrar_bitacoras():
    data = request.get_json()
    query = data.get('query', '').lower()
    try:
        bitacoras = Bitacora_service.obtener_registros_bitacoras()

        # Filtrar bitacoras por nombre
        bitacoras_filtradas = [
            bitacora.to_dict() for bitacora in bitacoras
            if query in bitacora.nombre.lower()
        ]

        return jsonify({'bitacoras': bitacoras_filtradas})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500


@inspeccion_campo_bp.route('/obtener_zona_por_bitacora/<id_bitacora>', methods=['GET'])
def obtener_zona_por_cuaderno(id_bitacora):
    try:
        bitacora = Bitacora_service.obtener_bitacora_por_id(id_bitacora)
        if not bitacora:
            return jsonify({'error': 'Bitacora no encontrada'}), 404

        return jsonify({'bitacoras': bitacora})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@inspeccion_campo_bp.route('/agregar_inspeccion/<id>', methods=['POST'])
def agregar_inspeccion(id):
    print("entre a agregar_inspeccion")
    form = InspeccionForm()
    if form.validate_on_submit():
        try:
            # Obtener la inspección de campo
            inspeccion_campo = InspeccionCampoService.obtener_inspeccion_campo_por_id(id)
            if not inspeccion_campo:
                flash('Inspección de campo no encontrada', 'danger')
                return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))
            
            # Generar el ID único para la nueva inspección
            nuevo_id = f'inspeccion-{len(inspeccion_campo.get("listInspeccion", [])) + 1}'
            
            # Crear el objeto inspección con el ID único
            inspeccion = {
                'id': nuevo_id,
                'inspeccion': form.inspeccion.data,
                'fecha_inicio': form.fecha_inicio.data.strftime('%Y-%m-%d'),
                'hora_inicio': form.hora_inicio.data.strftime('%H:%M'),
                'hora_fin': form.hora_fin.data.strftime('%H:%M'),
                'observ': form.observ.data,
                'listLayerId': form.listLayerId.data,
                'listOutLayerId': form.listOutLayerId.data
            }
            
            # Agregar la nueva inspección a la lista de inspecciones de la inspección de campo
            InspeccionCampoService.agregar_inspeccion_a_inspeccion_campo(id, inspeccion)

            flash('Inspección agregada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al agregar inspección: {e}', 'danger')
    else:
        flash('Error en el formulario', 'danger')
    return redirect(url_for('ins_campo_route.ver_inspeccion_campo', id=id))


@inspeccion_campo_bp.route('/ver/<id>', methods=['GET'])
def ver_inspeccion_campo(id):
    form = InspeccionForm()
    try:
        inspeccion_campo = InspeccionCampoService.obtener_inspeccion_campo_por_id(id)
        print(inspeccion_campo)
        if not inspeccion_campo:
            flash('Inspección de campo no encontrada', 'danger')
            return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))

        form.inspeccion.data = inspeccion_campo.get('inspeccion')
        form.fecha_inicio.data = inspeccion_campo.get('fecha_inicio')
        form.hora_inicio.data = inspeccion_campo.get('hora_inicio')
        form.hora_fin.data = inspeccion_campo.get('hora_fin')
        form.observ.data = inspeccion_campo.get('observ')

        return render_template('/inspeccion_campo/update_inspeccion_campo.html', inspeccion_campo=inspeccion_campo, form=form)
    except Exception as e:
        flash(f'Error al cargar la inspección de campo: {e}', 'danger')
        return redirect(url_for('ins_campo_route.mostrar_inspeccion_campo', id=id))


@inspeccion_campo_bp.route('/obtener_inspecciones/<id>', methods=['GET'])
def obtener_inspecciones(id):
    try:
        inspeccion_campo = InspeccionCampoService.obtener_inspeccion_campo_por_id(id)
        if not inspeccion_campo:
            return jsonify({"error": "Inspección de campo no encontrada"}), 404

        inspecciones = inspeccion_campo.get('listInspeccion', [])

        return jsonify({
            "inspecciones": inspecciones,
        })
    
    except Exception as e:
        print(f'Error al obtener inspecciones: {e}')
        return jsonify({'error': str(e)}), 500


@inspeccion_campo_bp.route('/actualizar_inspeccion/<inspeccion_campo_id>/<inspeccion_id>', methods=['POST'])
def actualizar_inspeccion(inspeccion_campo_id, inspeccion_id):
    print("entrando a la ruta de actualizar inspección")
    form = InspeccionForm()
    print("imrpimiendo despues de form = InspeccionForm()")
    if form.validate_on_submit():
        print("entrando dentro del if de form.validate_on_submit():")
        try:
            inspeccion = {
                'inspeccion': form.inspeccion.data,
                'fecha_inicio': form.fecha_inicio.data.strftime('%Y-%m-%d'),
                'hora_inicio': form.hora_inicio.data.strftime('%H:%M'),
                'hora_fin': form.hora_fin.data.strftime('%H:%M'),
                'observ': form.observ.data,
                'listLayerId': form.listLayerId.data,
                'listOutLayerId': form.listOutLayerId.data,
                'id': inspeccion_id
            }
            
            # Actualizar la inspección en la colección de Firestore
            InspeccionCampoService.actualizar_inspeccion(inspeccion_campo_id, inspeccion_id, inspeccion)
            flash('Inspección actualizada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al actualizar inspección: {e}', 'danger')
    else:
        print("Error en el formulario")
        print(form.errors)  # Imprimir los errores del formulario
        flash('Error en el formulario', 'danger')
    return redirect(url_for('ins_campo_route.mostrar_inspeccion_campo', id=inspeccion_campo_id))

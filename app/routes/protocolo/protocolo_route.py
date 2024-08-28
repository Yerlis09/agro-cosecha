from flask import render_template, url_for, flash, request, jsonify
from werkzeug.utils import redirect
import json

from . import protocolo_bp
from src.services.protocolo_service.protocolo_service import ProtocoloService
from src.services.bitacora_service.bitacora_service import Bitacora_service
from src.validator_form.protocolo_form_validator import ProtocoloForm


@protocolo_bp.route('/insertar_protocolo', methods=['GET', 'POST'])
def insertar_protocolo():
    form = ProtocoloForm()
    if form.validate_on_submit():
        try:
            protocolo = get_protocolo_dic_from(form)
            ProtocoloService.agregar_nuevo_protocolo(protocolo)
            
            return redirect(url_for('protocolo_route.mostrar_protocolos'))
        except ValueError as e:
            flash(str(e))
            return render_template('/protocolo/add_protocolo.html', form=form)
        except Exception as e:
            flash(f"Error al guardar los datos: {e}")
            return render_template('/protocolo/add_protocolo.html', form=form)
    else:
        print("Errores en el formulario:", form.errors)
    return render_template('/protocolo/add_protocolo.html', form=form)


@protocolo_bp.route('/mostrar_registros_protocolos', methods=['GET', 'POST'])
def mostrar_protocolos():
    form = ProtocoloForm()
    try:
        protocolos = ProtocoloService.obtener_registros_protocolos()

        # Validar y setear campos específicos si es necesario
        for protocolo in protocolos:
            # Convertir nombre_bitacora a cadena si es una tupla
            if isinstance(protocolo.nombre_bitacora, tuple):
                try:
                    protocolo.nombre_bitacora = str(protocolo.nombre_bitacora[0])
                except (ValueError, IndexError) as e:
                    print(f"Error al convertir nombre_bitacora de tupla a string: {protocolo.nombre_bitacora}, Error: {e}")
                    protocolo.nombre_bitacora = ""  # Valor predeterminado en caso de error

    except Exception as e:
        flash(f"Error al obtener los protocolos: {e}", "danger")
        protocolos = []
    return render_template('/protocolo/protocolo_form.html', form=form, protocolos=protocolos)


@protocolo_bp.route('/update/<id>', methods=['GET', 'POST'])
def actualizar_protocolo(id):
    form = ProtocoloForm()
    if form.validate_on_submit():
        datosUpdate = get_protocolo_dic_from(form)
        try:
            ProtocoloService.modificar_un_protocolo(id, datosUpdate)
            flash('Protocolo actualizado exitosamente', 'success')
            return redirect(url_for('protocolo_route.mostrar_protocolos'))
        except Exception as e:
            flash(f'Error al actualizar protocolo: {e}', 'danger')
    else:
        if request.method == 'POST':
            print("Error en el formulario")
            print(form.errors)  # Imprimir los errores del formulario
            flash('Error en el formulario', "danger")
        else:
            try:
                protocolo = ProtocoloService.obtener_protocolo_por_id(id)
                # Parsear lista_herramientas si es una cadena JSON
                if isinstance(protocolo['lista_herramientas'], str):
                    protocolo['lista_herramientas'] = json.loads(protocolo['lista_herramientas'])
                # Parsear lista_vuelos si es una cadena JSON
                if isinstance(protocolo['lista_vuelos'], str):
                    protocolo['lista_vuelos'] = json.loads(protocolo['lista_vuelos'])
                # Parsear lista_detectores si es una cadena JSON
                if isinstance(protocolo['lista_detectores'], str):
                    protocolo['lista_detectores'] = json.loads(protocolo['lista_detectores'])
                # Parsear lista_detectores si es una cadena JSON
                if isinstance(protocolo['lista_inspecciones'], str):
                    protocolo['lista_inspecciones'] = json.loads(protocolo['lista_inspecciones'])
                
                form = ProtocoloForm(data=protocolo)
            except Exception as e:
                flash(f'Error al obtener datos del protocolo: {e}', 'danger')
                return redirect(url_for('protocolo_route.mostrar_protocolos'))

    return render_template('/protocolo/update_protocolo.html', form=form, protocolo=protocolo)



@protocolo_bp.route('/delete/<id>', methods=['POST'])
def delete_protocolo(id):
    try:
        ProtocoloService.eliminar_protocolo(id)
        print('Protocolo eliminado exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar protocolo: {e}', 'danger')
    return redirect(url_for('protocolo_route.mostrar_protocolos'))

def get_protocolo_dic_from(form):
    # Verifica si algún campo obligatorio está vacío
    if not form.dat_bitacora.data:
        raise ValueError("El campo 'nombre de bitácora' no puede estar vacío")
    if not form.id_cuaderno.data:
        raise ValueError("El campo 'id de bitácora' no puede estar vacío")
    if not form.fecha_inicio_pres.data:
        raise ValueError("El campo 'fecha de inicio' no puede estar vacío")
    if not form.fecha_fin_pres.data:
        raise ValueError("El campo 'fecha de fin' no puede estar vacío")
    if not form.nombre_pres.data:
        raise ValueError("El campo 'nombre de la prescripción' no puede estar vacío")
    if not form.alt_no_quimica.data:
        raise ValueError("El campo 'alternativa no química' no puede estar vacío")
    if not form.detec_plaga.data:
        raise ValueError("El campo 'detección de plaga' no puede estar vacío")
    if not form.hidrat_cultivo.data:
        raise ValueError("El campo 'hidratación del cultivo' no puede estar vacío")
    if not form.nutren_suelo.data:
        raise ValueError("El campo 'nutrición del suelo' no puede estar vacío")
    if not form.dosis_util.data:
        raise ValueError("El campo 'dosis útil' no puede estar vacío")
    if not form.infor_obt_desde.data:
        raise ValueError("El campo 'información obtenida desde' no puede estar vacío")
    if not form.list_herra_select.data:
        raise ValueError("El campo 'lista de herramientas' no puede estar vacío")
    
    return {
        'nombre_bitacora': form.dat_bitacora.data,
        'id_bitacora': form.id_cuaderno.data,
        'fecha_inicio_pres': form.fecha_inicio_pres.data,
        'fecha_fin_pres': form.fecha_fin_pres.data,
        'nombre_pres': form.nombre_pres.data,
        'alt_no_quimica': form.alt_no_quimica.data,
        'descr_alt_no_quimica': form.descr_alt_no_quimica.data,
        'detec_plaga': form.detec_plaga.data,
        'hidrat_cultivo': form.hidrat_cultivo.data,
        'nutren_suelo': form.nutren_suelo.data,
        'dosis_util': form.dosis_util.data,
        'infor_obt_desde': form.infor_obt_desde.data,
        'lista_detectores': form.list_detect_select.data,
        'lista_vuelos': form.list_vuelo_select.data,
        'lista_inspecciones': form.list_insp_select.data,
        'lista_herramientas': form.list_herra_select.data
    }


@protocolo_bp.route('/filtrar_bitacoras', methods=['POST'])
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


@protocolo_bp.route('/filtrar_planes_vuelo', methods=['POST'])
def filtrar_planes_vuelo():
    data = request.get_json()
    cuaderno_id = data.get('cuaderno_id')
    query = data.get('query', '').lower()
    try:
        planes_vuelo = ProtocoloService.filtrar_planes_vuelo_por_cuaderno(cuaderno_id)
        # Filtrar vuelos por nombre
        planes_filtrados = [
            plan_vuelo for plan_vuelo in planes_vuelo
            if query in plan_vuelo['nombre'].lower()
        ]

        return jsonify({'planes_vuelo': planes_filtrados})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500

@protocolo_bp.route('/filtrar_detectores', methods=['POST'])
def filtrar_detectores():
    data = request.get_json()
    cuaderno_id = data.get('cuaderno_id')
    query = data.get('query', '').lower()
    try:
        detectores = ProtocoloService.filtrar_detectores_por_cuaderno(cuaderno_id)
        # Filtrar detectores por nombre
        detectores_filtrados = [
            detector for detector in detectores
            if query in detector['nombre'].lower()
        ]

        return jsonify({'detectores': detectores_filtrados})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500

@protocolo_bp.route('/filtrar_inspecciones_campo', methods=['POST'])
def filtrar_inspecciones_campo():
    data = request.get_json()
    cuaderno_id = data.get('cuaderno_id')
    query = data.get('query', '').lower()
    try:
        inspecciones_campo = ProtocoloService.filtrar_inspecciones_campo_por_cuaderno(cuaderno_id)

        # Filtrar inspecciones_campo por nombre
        inspecciones_filtradas = [
            inspeccion for inspeccion in inspecciones_campo
            if query in inspeccion['nombre'].lower()
        ]

        return jsonify({'inspecciones_campo': inspecciones_filtradas})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500

@protocolo_bp.route('/filtrar_herramientas', methods=['POST'])
def filtrar_herramientas():
    data = request.get_json()
    cuaderno_id = data.get('cuaderno_id')
    query = data.get('query', '').lower()
    try:
        herramientas = ProtocoloService.filtrar_herramientas_por_cuaderno(cuaderno_id)
        # Filtrar herramientas por nombre
        herramientas_filtradas = [
            herramienta for herramienta in herramientas
            if query in herramienta['nombre'].lower()
        ]

        return jsonify({'herramientas': herramientas_filtradas})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500
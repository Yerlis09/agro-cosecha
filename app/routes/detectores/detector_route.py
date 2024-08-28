from flask import render_template, url_for, flash, request, jsonify
from werkzeug.utils import redirect
import json
from datetime import datetime

from . import detectores_bp
from src.services.detectores_service.detector_service import DetectorService
from src.services.bitacora_service.bitacora_service import Bitacora_service
from src.validator_form.detector_form_validator import DetectorForm
from src.validator_form.sensor_form_validator import SensorForm


@detectores_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = DetectorForm()

    if form.validate_on_submit():
        try:
            detector = get_detector_dic_from(form)
            
            DetectorService.agregar_nuevo_detector(detector)
            return redirect(url_for('detectores_route.mostrar_detectores'))
        except ValueError as e:
            flash(str(e))
            return render_template('/detector/detector_form.html', form=form)
        except Exception as e:
            flash(f"Error al guardar los datos: {e}")
            return render_template('/detector/detector_form.html', form=form)
    else:
        print(form.errors)
    return render_template('/detector/add_detector_form.html', form=form)


@detectores_bp.route('/mostrar_registros_detectores', methods=['GET', 'POST'])
def mostrar_detectores():
    form = DetectorForm()

    try:
        detectores = DetectorService.obtener_registros_detectores()

         # Validar y setear 'sensores_realizados'
        for detector in detectores:
            print(f"Detector antes del if: {detector.detectores_realizados}")
            if hasattr(detector, 'listSensor') and isinstance(detector.listSensor, list):
                print("entre al if")
                detector.detectores_realizados = len(detector.listSensor)
            else:
                print("entre al else de listSensor no existente")
                detector.detectores_realizados = 0

            # Asegurarse de que detectores_estimados es un entero
            if isinstance(detector.detectores_estimados, tuple):
                print("entre al if de conversion de tupla a int de detectores_estimados")
                try:
                    detector.detectores_estimados = int(detector.detectores_estimados[0])
                except (ValueError, IndexError) as e:
                    print(f"Error al convertir detectores_estimados de tupla a int: {detector.detectores_estimados}, Error: {e}")
                    detector.detectores_estimados = 0  # Valor predeterminado en caso de error

            # Convertir nombre_bitacora a cadena si es una tupla
            if isinstance(detector.nombre_bitacora, tuple):
                print("entre al if de conversion de tupla a string de nombre_bitacora")
                try:
                    detector.nombre_bitacora = str(detector.nombre_bitacora[0])
                except (ValueError, IndexError) as e:
                    print(f"Error al convertir nombre_bitacora de tupla a string: {detector.nombre_bitacora}, Error: {e}")
                    detector.nombre_bitacora = ""  # Valor predeterminado en caso de error

    except Exception as e:
        flash(f"Error al obtener los detectores: {e}", "danger")
        detectores = []
    return render_template('/detector/detector_form.html', form=form, detectores=detectores)


@detectores_bp.route('/mostrar_detector/<id>', methods=['GET', 'POST'])
def mostrar_detector(id):
    form = DetectorForm()
    sensor_form = SensorForm()
    try:
        detector = DetectorService.obtener_detector_por_id(id)
        if not detector:
            flash('Detector no encontrado', 'danger')
            return redirect(url_for('detectores_route.mostrar_detectores'))

        # Convertir la fecha de str a datetime.date
        if isinstance(detector['fecha'], str):
            detector['fecha'] = datetime.strptime(detector['fecha'], '%Y-%m-%d').date()


        # Prellenar el formulario con los datos del detector
        form.nombre.data = detector['nombre']
        form.fecha.data = detector['fecha']
        form.duracion.data = detector['duracion']
        form.periocidad.data = detector['periocidad']
        form.dat_bitacora.data = detector['nombre_bitacora']
        form.id_cuaderno.data = detector['id_bitacora']

        return render_template('/detector/update_detector.html', form=form, detector=detector, sensor_form=sensor_form)
    except Exception as e:
        flash(f'Error al cargar el detector: {e}', 'danger')
        return redirect(url_for('detectores_route.mostrar_detectores'))


@detectores_bp.route('/delete/<id>', methods=['POST'])
def delete_detector(id):
    try:
        DetectorService.eliminar_detector(id)
        print('Detector eliminado exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar detector: {e}', 'danger')
    return redirect(url_for('detectores_route.mostrar_detectores'))


def get_detector_dic_from(form):
    # Verifica si algún campo obligatorio está vacío
    if not form.nombre.data:
        raise ValueError("El campo 'nombre detector' no puede estar vacío")
    if not form.fecha.data:
        raise ValueError("El campo 'fecha detector' no puede estar vacío")
    if not form.duracion.data:
        raise ValueError("El campo 'duracion' no puede estar vacío")
    if not form.periocidad.data:
        raise ValueError("El campo 'periocidad' no puede estar vacío")
    if not form.dat_bitacora.data:
        raise ValueError("El campo 'nombre de bitacora' no puede estar vacío")
    if not form.id_cuaderno.data:
        raise ValueError("El campo 'id_cuaderno' no puede estar vacío")
    if not form.sensores_estimados.data:
        raise ValueError("El campo 'sensores_estimados' no puede estar vacío")
    
    return {
        'nombre': form.nombre.data,
        'fecha': form.fecha.data,
        'duracion': form.duracion.data,
        'periocidad': form.periocidad.data,
        'nombre_bitacora': form.dat_bitacora.data,
        'id_bitacora': form.id_cuaderno.data,
        'detectores_estimados': form.sensores_estimados.data
    }


@detectores_bp.route('/filtrar_bitacoras', methods=['POST'])
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


@detectores_bp.route('/obtener_zona_por_bitacora/<id_bitacora>', methods=['GET'])
def obtener_zona_por_cuaderno(id_bitacora):
    try:
        bitacora = Bitacora_service.obtener_bitacora_por_id(id_bitacora)
        if not bitacora:
            return jsonify({'error': 'Bitacora no encontrada'}), 404

        return jsonify({'bitacoras': bitacora})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@detectores_bp.route('/agregar_sensor/<id>', methods=['POST'])
def agregar_sensor(id):
    print("entre a agregar_sensor")
    form = SensorForm()
    if form.validate_on_submit():
        try:
            # Obtener el detector
            detector = DetectorService.obtener_detector_por_id(id)
            if not detector:
                flash('Detector no encontrado', 'danger')
                return redirect(url_for('detectores_route.mostrar_detectores'))
            
            # Generar el ID único para el nuevo sensor
            nuevo_id = f'sensor-{len(detector.get("listSensor", [])) + 1}'
            
            # Crear el objeto sensor con el ID único
            sensor = {
                'id': nuevo_id,
                'sensor': form.sensor.data,
                'fecha_inicio': form.fecha_inicio.data.strftime('%Y-%m-%d'),
                'hora_inicio': form.hora_inicio.data.strftime('%H:%M'),
                'hora_fin': form.hora_fin.data.strftime('%H:%M'),
                'observ': form.observ.data,
                'listLayerId': form.listLayerId.data,
                'listOutLayerId': form.listOutLayerId.data
            }
            
            # Agregar el nuevo sensor a la lista de sensores del detector
            DetectorService.agregar_sensor_a_detector(id, sensor)

            detector = DetectorService.obtener_detector_por_id(id)

             # Validar y setear 'sensores_realizados'
            if 'listSensor' in detector and isinstance(detector['listSensor'], list):
                detector['sensores_realizados'] = len(detector['listSensor'])
            else:
                detector['sensores_realizados'] = 0

            # Actualizar sensores_realizados en la base de datos
            DetectorService.actualizar_sensores_realizados(id, detector['sensores_realizados'])

            flash('Sensor agregado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al agregar sensor: {e}', 'danger')
    else:
        flash('Error en el formulario', 'danger')
    return redirect(url_for('detectores_route.ver_detector', id=id))


@detectores_bp.route('/ver/<id>', methods=['GET'])
def ver_detector(id):
    form = SensorForm()
    try:
        detector = DetectorService.obtener_detector_por_id(id)
        print(detector)
        if not detector:
            flash('Detector no encontrado', 'danger')
            return redirect(url_for('detectores_route.mostrar_detectores'))

        # Populate form with existing detector data
        form.sensor.data = detector.get('sensor')
        form.fecha_inicio.data = detector.get('fecha_inicio')
        form.hora_inicio.data = detector.get('hora_inicio')
        form.hora_fin.data = detector.get('hora_fin')
        form.ulr_img.data = detector.get('ulr_img')
        form.observ.data = detector.get('observ')

        return render_template('/detectores/update_detector.html', detector=detector, form=form)
    except Exception as e:
        flash(f'Error al cargar el detector: {e}', 'danger')
        return redirect(url_for('detectores_route.mostrar_detector', id=id))


@detectores_bp.route('/obtener_sensores/<id>', methods=['GET'])
def obtener_sensores(id):
    try:
        detector = DetectorService.obtener_detector_por_id(id)
        if not detector:
            return jsonify({"error": "Detector no encontrado"}), 404

        sensores = detector.get('listSensor', [])
        sensores_realizados = len(sensores)

        # Verificar si detectores_estimados es una tupla y convertirlo a entero
        if isinstance(detector.get('detectores_estimados'), tuple):
            print("entre al if de conversion de tupla a int de detectores_estimados")
            try:
                detector['detectores_estimados'] = int(detector['detectores_estimados'][0])
            except (ValueError, IndexError) as e:
                print(f"Error al convertir detectores_estimados de tupla a int: {detector['detectores_estimados']}, Error: {e}")
                detector['detectores_estimados'] = 0  # Valor predeterminado en caso de error

        detectores_estimados = detector.get('detectores_estimados', 0)

        return jsonify({
            "sensores": sensores,
            "sensores_realizados": sensores_realizados,
            "detectores_estimados": detectores_estimados
        })
    
    except Exception as e:
        print(f'Error al obtener sensores: {e}')
        return jsonify({'error': str(e)}), 500


@detectores_bp.route('/actualizar_sensor/<detector_id>/<sensor_id>', methods=['POST'])
def actualizar_sensor(detector_id, sensor_id):
    print("entrando a la ruta de actualizar sensor")
    form = SensorForm()
    print("imrpimiendo despues de form = SensorForm()")
    if form.validate_on_submit():
        print("entrando dentro del if de form.validate_on_submit():")
        try:
            sensor = {
                'sensor': form.sensor.data,
                'fecha_inicio': form.fecha_inicio.data.strftime('%Y-%m-%d'),
                'hora_inicio': form.hora_inicio.data.strftime('%H:%M'),
                'hora_fin': form.hora_fin.data.strftime('%H:%M'),
                'observ': form.observ.data,
                'listLayerId': form.listLayerId.data,
                'listOutLayerId': form.listOutLayerId.data,
                'id': sensor_id
            }
            
            # Actualizar el sensor en la colección de Firestore
            DetectorService.actualizar_sensor(detector_id, sensor_id, sensor)
            flash('Sensor actualizado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al actualizar sensor: {e}', 'danger')
    else:
        print("Error en el formulario")
        print(form.errors)  # Imprimir los errores del formulario
        flash('Error en el formulario', 'danger')
    return redirect(url_for('detectores_route.mostrar_detector', id=detector_id))

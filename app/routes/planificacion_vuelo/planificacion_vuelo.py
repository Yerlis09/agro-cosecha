from flask import render_template, url_for, flash, request, jsonify
from werkzeug.utils import redirect
import json
from datetime import datetime


from . import plan_vuelo_bp
from src.services.planificacion_vuelo_service.planificacion_vuelo import PlanVueloService
from src.services.bitacora_service.bitacora_service import Bitacora_service
from src.validator_form.planificacion_vuelo_form_validator import PlanVueloForm
from src.validator_form.vuelo_form_validator import VueloForm


@plan_vuelo_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = PlanVueloForm()

    if form.validate_on_submit():
        try:
            plan_vuelo = get_plan_vuelo_dic_from(form)
            
            PlanVueloService.agregar_nuevo_plan_vuelo(plan_vuelo)
            return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))
        except ValueError as e:
            flash(str(e))
            return render_template('/plan_vuelo/plan_vuelo_form.html', form=form)
        except Exception as e:
            flash(f"Error al guardar los datos: {e}")
            return render_template('/plan_vuelo/plan_vuelo_form.html', form=form)
    else:
        print(form.errors)
    return render_template('/plan_vuelo/add_plan_vuelo_form.html', form=form)


@plan_vuelo_bp.route('/mostrar_registros_plan_vuelos', methods=['GET', 'POST'])
def mostrar_plan_vuelos():
    form = PlanVueloForm()

    try:
        plan_vuelos = PlanVueloService.obtener_registros_plan_vuelos()

         # Validar y setear 'vuelos_realizados'
        for plan_vuelo in plan_vuelos:
            print(f"Plan vuelo antes del if: {plan_vuelo.vuelos_realizados}")
            if hasattr(plan_vuelo, 'listVuelo') and isinstance(plan_vuelo.listVuelo, list):
                print("entre al if")
                plan_vuelo.vuelos_realizados = len(plan_vuelo.listVuelo)
            else:
                print("entre al else de listVuelo no existente")
                plan_vuelo.vuelos_realizados = 0

            # Asegurarse de que vuelos_estimados es un entero
            if isinstance(plan_vuelo.vuelos_estimados, tuple):
                print("entre al if de conversion de tupla a int de vuelos estimados")
                try:
                    plan_vuelo.vuelos_estimados = int(plan_vuelo.vuelos_estimados[0])
                except (ValueError, IndexError) as e:
                    print(f"Error al convertir vuelos_estimados de tupla a int: {plan_vuelo.vuelos_estimados}, Error: {e}")
                    plan_vuelo.vuelos_estimados = 0  # Valor predeterminado en caso de error

            # Convertir nombre_bitacora a cadena si es una tupla
            if isinstance(plan_vuelo.nombre_bitacora, tuple):
                print("entre al if de conversion de tupla a string de nombre_bitacora")
                try:
                    plan_vuelo.nombre_bitacora = str(plan_vuelo.nombre_bitacora[0])
                except (ValueError, IndexError) as e:
                    print(f"Error al convertir nombre_bitacora de tupla a string: {plan_vuelo.nombre_bitacora}, Error: {e}")
                    plan_vuelo.nombre_bitacora = ""  # Valor predeterminado en caso de error

    except Exception as e:
        flash(f"Error al obtener los plan vuelos: {e}", "danger")
        plan_vuelos = []
    return render_template('/plan_vuelo/plan_vuelo_form.html', form=form, plan_vuelos=plan_vuelos)


@plan_vuelo_bp.route('/mostrar_plan_vuelo/<id>', methods=['GET', 'POST'])
def mostrar_plan_vuelo(id):
    form = PlanVueloForm()
    vuelo_form = VueloForm()
    try:
        plan_vuelo = PlanVueloService.obtener_plan_vuelo_por_id(id)
        if not plan_vuelo:
            flash('Plan de vuelo no encontrado', 'danger')
            return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))

        # Convertir la fecha de str a datetime.date
        if isinstance(plan_vuelo['fecha'], str):
            plan_vuelo['fecha'] = datetime.strptime(plan_vuelo['fecha'], '%Y-%m-%d').date()


        # Prellenar el formulario con los datos del plan_vuelo
        form.nombre.data = plan_vuelo['nombre']
        form.fecha.data = plan_vuelo['fecha']
        form.duracion.data = plan_vuelo['duracion']
        form.periocidad.data = plan_vuelo['periocidad']
        form.dat_bitacora.data = plan_vuelo['nombre_bitacora']
        form.id_cuaderno.data = plan_vuelo['id_bitacora']

        return render_template('/plan_vuelo/update_plan_vuelo.html', form=form, plan_vuelo=plan_vuelo, vuelo_form=vuelo_form)
    except Exception as e:
        flash(f'Error al cargar el plan de vuelo: {e}', 'danger')
        return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))

 
@plan_vuelo_bp.route('/delete/<id>', methods=['POST'])
def delete_plan_vuelo(id):
    try:
        PlanVueloService.eliminar_plan_vuelo(id)
        print('PlanVuelo eliminado exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar plan_vuelo: {e}', 'danger')
    return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))


def get_plan_vuelo_dic_from(form):
    # Verifica si algún campo obligatorio está vacío
    if not form.nombre.data:
        raise ValueError("El campo 'nombre vuelo' no puede estar vacío")
    if not form.fecha.data:
        raise ValueError("El campo 'fecha vuelo' no puede estar vacío")
    if not form.duracion.data:
        raise ValueError("El campo 'duracion' no puede estar vacío")
    if not form.periocidad.data:
        raise ValueError("El campo 'periocidad' no puede estar vacío")
    if not form.dat_bitacora.data:
        raise ValueError("El campo 'nombre de bitacora' no puede estar vacío")
    if not form.id_cuaderno.data:
        raise ValueError("El campo 'id_cuaderno' no puede estar vacío")
    if not form.vuelos_estimados.data:
        raise ValueError("El campo 'vuelos_estimados' no puede estar vacío")
    
    return {
        'nombre': form.nombre.data,
        'fecha': form.fecha.data,
        'duracion': form.duracion.data,
        'periocidad': form.periocidad.data,
        'nombre_bitacora': form.dat_bitacora.data,
        'id_bitacora': form.id_cuaderno.data,
        'vuelos_estimados': form.vuelos_estimados.data
    }


@plan_vuelo_bp.route('/filtrar_bitacoras', methods=['POST'])
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
 

@plan_vuelo_bp.route('/obtener_zona_por_bitacora/<id_bitacora>', methods=['GET'])
def obtener_zona_por_cuaderno(id_bitacora):
    try:
        bitacora = Bitacora_service.obtener_bitacora_por_id(id_bitacora)
        if not bitacora:
            return jsonify({'error': 'Bitacora no encontrada'}), 404

        return jsonify({'bitacoras': bitacora})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@plan_vuelo_bp.route('/agregar_vuelo/<id>', methods=['POST'])
def agregar_vuelo(id):
    form = VueloForm()
    if form.validate_on_submit():
        try:
            # Obtener el plan de vuelo
            plan_vuelo = PlanVueloService.obtener_plan_vuelo_por_id(id)
            if not plan_vuelo:
                flash('Plan de vuelo no encontrado', 'danger')
                return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))
            
            # Generar el ID único para el nuevo vuelo
            nuevo_id = f'vuelo-{len(plan_vuelo.get("listVuelo", [])) + 1}'
            
            # Crear el objeto vuelo con el ID único
            vuelo = {
                'id': nuevo_id,
                'vuelo': form.vuelo.data,
                'fecha_inicio': form.fecha_inicio.data.strftime('%Y-%m-%d'),
                'hora_inicio': form.hora_inicio.data.strftime('%H:%M'),
                'hora_fin': form.hora_fin.data.strftime('%H:%M'),
                'ulr_img': form.ulr_img.data,
                'observ': form.observ.data,
                'listLayerId': form.listLayerId.data,
                'listOutLayerId': form.listOutLayerId.data
            }
            
            # Agregar el nuevo vuelo a la lista de vuelos del plan
            PlanVueloService.agregar_vuelo_a_plan(id, vuelo)

            plan_vuelo = PlanVueloService.obtener_plan_vuelo_por_id(id)

             # Validar y setear 'vuelos_realizados'
            if 'listVuelo' in plan_vuelo and isinstance(plan_vuelo['listVuelo'], list):
                plan_vuelo['vuelos_realizados'] = len(plan_vuelo['listVuelo'])
            else:
                plan_vuelo['vuelos_realizados'] = 0

            # Actualizar vuelos_realizados en la base de datos
            PlanVueloService.actualizar_vuelos_realizados(id, plan_vuelo['vuelos_realizados'])

            flash('Vuelo agregado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al agregar vuelo: {e}', 'danger')
    else:
        flash('Error en el formulario', 'danger')
    return redirect(url_for('plan_vuelo_route.ver_plan_vuelo', id=id))


@plan_vuelo_bp.route('/ver/<id>', methods=['GET'])
def ver_plan_vuelo(id):
    form = VueloForm()
    try:
        plan_vuelo = PlanVueloService.obtener_plan_vuelo_por_id(id)
        print(plan_vuelo)
        if not plan_vuelo:
            flash('Plan de vuelo no encontrado', 'danger')
            return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))

        # Populate form with existing plan data
        form.vuelo.data = plan_vuelo.get('vuelo')
        form.fecha_inicio.data = plan_vuelo.get('fecha_inicio')
        form.hora_inicio.data = plan_vuelo.get('hora_inicio')
        form.hora_fin.data = plan_vuelo.get('hora_fin')
        form.ulr_img.data = plan_vuelo.get('ulr_img')
        form.observ.data = plan_vuelo.get('observ')

        return render_template('/plan_vuelo/update_plan_vuelo.html', plan_vuelo=plan_vuelo, form=form)
    except Exception as e:
        flash(f'Error al cargar el plan de vuelo: {e}', 'danger')
        return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelo', id=id))


@plan_vuelo_bp.route('/obtener_vuelos/<id>', methods=['GET'])
def obtener_vuelos(id):
    try:
        plan_vuelo = PlanVueloService.obtener_plan_vuelo_por_id(id)
        if not plan_vuelo:
            return jsonify({"error": "Plan de vuelo no encontrado"}), 404

        vuelos = plan_vuelo.get('listVuelo', [])
        vuelos_realizados = len(vuelos)

        # Verificar si vuelos_estimados es una tupla y convertirlo a entero
        if isinstance(plan_vuelo.get('vuelos_estimados'), tuple):
            print("entre al if de conversion de tupla a int de vuelos estimados")
            try:
                plan_vuelo['vuelos_estimados'] = int(plan_vuelo['vuelos_estimados'][0])
            except (ValueError, IndexError) as e:
                print(f"Error al convertir vuelos_estimados de tupla a int: {plan_vuelo['vuelos_estimados']}, Error: {e}")
                plan_vuelo['vuelos_estimados'] = 0  # Valor predeterminado en caso de error

        vuelos_estimados = plan_vuelo.get('vuelos_estimados', 0)


        return jsonify({
            "vuelos": vuelos,
            "vuelos_realizados": vuelos_realizados,
            "vuelos_estimados": vuelos_estimados
        })
    
    except Exception as e:
        print(f'Error al obtener vuelos: {e}')
        return jsonify({'error': str(e)}), 500


@plan_vuelo_bp.route('/actualizar_vuelo/<plan_vuelo_id>/<vuelo_id>', methods=['POST'])
def actualizar_vuelo(plan_vuelo_id, vuelo_id):
    print("entrando a la ruta de actualizar vuelo")
    form = VueloForm()
    print("imrpimiendo despues de form = VueloForm()")
    if form.validate_on_submit():
        print("entrando dentro del if de form.validate_on_submit():")
        try:
            vuelo = {
                'vuelo': form.vuelo.data,
                'fecha_inicio': form.fecha_inicio.data.strftime('%Y-%m-%d'),
                'hora_inicio': form.hora_inicio.data.strftime('%H:%M'),
                'hora_fin': form.hora_fin.data.strftime('%H:%M'),
                'ulr_img': form.ulr_img.data,
                'observ': form.observ.data,
                'listLayerId': form.listLayerId.data,
                'listOutLayerId': form.listOutLayerId.data,
                'id': vuelo_id
            }
            
            # Actualizar el vuelo en la colección de Firestore
            PlanVueloService.actualizar_vuelo(plan_vuelo_id, vuelo_id, vuelo)
            flash('Vuelo actualizado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al actualizar vuelo: {e}', 'danger')
    else:
        flash('Error en el formulario', 'danger')
    return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelo', id=plan_vuelo_id))
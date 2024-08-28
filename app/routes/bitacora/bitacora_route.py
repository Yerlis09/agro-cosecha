from flask import render_template, url_for, flash, request, jsonify
from werkzeug.utils import redirect
import json

from . import bitacora_bp
from src.services.bitacora_service.bitacora_service import Bitacora_service
from src.services.cliente_service.cliente_service import Cliente_service
from src.services.zona_service.zona_service import ZonaService
from src.services.herramienta_service.herramienta_service import Herramienta_service
from src.validator_form.bitacora_form_validator import BitacoraForm


@bitacora_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = BitacoraForm()

    if form.validate_on_submit():
        try:
            bitacora = get_bitacora_dic_from(form)
            bitacora['lista_parcelas'] = json.loads(form.lista_parcelas.data)  # Convertir a array
        
            print("Bitacora creada:", bitacora) 
            
            Bitacora_service.agregar_nueva_bitacora(bitacora)
            return redirect(url_for('bitacora_route.mostrar_bitacoras'))
        except ValueError as e:
            flash(str(e))
            return render_template('/bitacora/bitacora_form.html', form=form)
        except Exception as e:
            flash(f"Error al guardar los datos: {e}")
            return render_template('/bitacora/bitacora_form.html', form=form)
    else:
        print(form.errors)
    return render_template('/bitacora/add_bitacora.html', form=form)


@bitacora_bp.route('/mostrar_registros_bitacoras', methods=['GET', 'POST'])
def mostrar_bitacoras():
    form = BitacoraForm()

    try:
        bitacoras = Bitacora_service.obtener_registros_bitacoras()

    except Exception as e:
        flash(f"Error al obtener los bitacoras: {e}", "danger")
        bitacoras = []
    return render_template('/bitacora/bitacora_form.html', form=form, bitacoras=bitacoras)


@bitacora_bp.route('/update/<id>', methods=['POST'])
def postUpdate(id):
    form = BitacoraForm()    
    datosUpdate = get_bitacora_dic_from(form)

    if not datosUpdate:
        flash("Bitacora no encontrado", "warning")

    if form.validate_on_submit():
        try:
            Bitacora_service.modificar_una_bitacora(id, datosUpdate)
            flash('Bitacora actualizado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al actualizar bitacora: {e}', 'danger')
    else:
        print(form.errors)
        flash('Error en el formulario', "danger")
    
    return redirect(url_for('bitacora_route.mostrar_bitacoras'))


@bitacora_bp.route('/delete/<id>', methods=['POST'])
def delete_bitacora(id):
    try:
        Bitacora_service.eliminar_bitacora(id)
        print('Bitacora eliminado exitosamente', 'success')
    except Exception as e:
        print(f'Error al eliminar bitacora: {e}', 'danger')
    return redirect(url_for('bitacora_route.mostrar_bitacoras'))


def get_bitacora_dic_from(form):
    # Verifica si algún campo obligatorio está vacío
    if not form.nombre_bitacora.data:
        raise ValueError("El campo 'nombre_bitacora' no puede estar vacío")
    if not form.fecha_apertura.data:
        raise ValueError("El campo 'fecha_apertura' no puede estar vacío")
    if not form.fecha_inicio.data:
        raise ValueError("El campo 'fecha_inicio' no puede estar vacío")
    if not form.fecha_fin.data:
        raise ValueError("El campo 'fecha_fin' no puede estar vacío")
    if not form.tipo_cultivo.data:
        raise ValueError("El campo 'tipo_cultivo' no puede estar vacío")
    if not form.nombre_encargado.data:
        raise ValueError("El campo 'nombre_encargado' no puede estar vacío")
    if not form.nro_ident_enc.data:
        raise ValueError("El campo 'nro_ident_enc' no puede estar vacío")
    if not form.personas_json.data:
        raise ValueError("El campo 'personas_json' no puede estar vacío")
    if not form.equipos_json.data:
        raise ValueError("El campo 'equipos_json' no puede estar vacío")
    if not form.nombre_zona.data:
        raise ValueError("El campo 'nombre_zona' no puede estar vacío")
    if not form.coordenadas_zona.data:
        raise ValueError("El campo 'coordenadas_zona' no puede estar vacío")
    if not form.id_zona.data:
        raise ValueError("El campo 'id_zona' no puede estar vacío")
    if not form.lista_parcelas.data:
        raise ValueError("El campo 'lista_parcelas' no puede estar vacío")   

    return {
        'nombre': form.nombre_bitacora.data,
        'fecha_apertura': form.fecha_apertura.data,
        'fecha_inicio': form.fecha_inicio.data,
        'fecha_fin': form.fecha_fin.data,
        'tipo_cultivo': form.tipo_cultivo.data,
        'nombre_encargado': form.nombre_encargado.data,
        'nro_ident_enc': form.nro_ident_enc.data,
        'listPersonas': form.personas_json.data,
        'nombre_zona': form.nombre_zona.data,
        'coordenadas_zona': form.coordenadas_zona.data,
        'id_zona': form.id_zona.data,
        'lista_parcelas': form.lista_parcelas.data,
        'lista_herramientas': form.equipos_json.data
    }


@bitacora_bp.route('/filtrar_clientes', methods=['POST'])
def filtrar_clientes():
    data = request.get_json()
    query = data.get('query', '').lower()

    try:
        clientes = Cliente_service.obtener_registros_clientes()

        # Filtrar clientes por nombre o identificación y roles específicos
        clientes_filtrados = [
            {
                'nombre': f"{cliente.nombres} {cliente.apellido}",
                'identificacion': cliente.identificacion
            } for cliente in clientes
            if (query in f"{cliente.nombres.lower()} {cliente.apellido.lower()}" or query in cliente.identificacion) 
        ]

        return jsonify({'clientes': clientes_filtrados})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500
    


@bitacora_bp.route('/filtrar_herramientas', methods=['POST'])
def filtrar_herramientas():
    data = request.get_json()
    query = data.get('query', '').lower()

    try:
        herramientas = Herramienta_service.obtener_registros_herramientas()
        # Filtrar herramientas por nombre 
        herramientas_filtradas = [
            {
                'nombre': herramienta.nombre_equipo,
                'funcionalidad': herramienta.funcionalidad_equipo
            } for herramienta in herramientas
            if (query in herramienta.nombre_equipo.lower()) 
        ]

        return jsonify({'herramientas': herramientas_filtradas})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500


@bitacora_bp.route('/filtrar_zonas', methods=['POST'])
def filtrar_zonas():
    data = request.get_json()
    query = data.get('query', '').lower()

    try:
        zonas = ZonaService.obtener_registros_zonas()

        # Filtrar zonas por nombre 
        zonas_filtradas = [
            {
                'document_id': zona.document_id, 
                'nombre': zona.nombre_zona,
                'lista_parcelas': zona.parcelas,
                'coordenadas_area': zona.ubicacion
            } for zona in zonas
            if (query in zona.nombre_zona.lower()) 
        ]

        return jsonify({'zonas': zonas_filtradas})
    except Exception as e:
        print('Error en el backend:', e)
        return jsonify({'error': str(e)}), 500
    
@bitacora_bp.route('/ver/<id>', methods=['GET'])
def ver_bitacora(id):
    print("ingresando al route de ver bitacora")
    form = BitacoraForm()
    try:
        bitacora = Bitacora_service.obtener_bitacora_por_id(id)
        print("impresion despues de obtener bitacora")
        if not bitacora:
            flash('Bitácora no encontrada', 'danger')
            return redirect(url_for('bitacora_route.mostrar_bitacoras'))

        print("aqui deberia renderizar a la pagina update")
        return render_template('/bitacora/update_bitacora.html', bitacora=bitacora, form=form)
    except Exception as e:
        flash(f'Error al cargar la bitácora: {e}', 'danger')
        return redirect(url_for('bitacora_route.mostrar_bitacoras'))

from flask import render_template, url_for, flash, jsonify, request, get_flashed_messages
import requests
from werkzeug.utils import redirect

## importacion para la autenticación de usuarios ##
import pyrebase
from app.auth_token import firebaseConfig
from src.services.firebase_config import get_firebase_auth  
import firebase_admin

from . import cliente_bp
from src.services.cliente_service.cliente_service import Cliente_service
from src.validator_form.client_update_form_validator import ClienteUpdateForm
from src.validator_form.client_create_form_validator import ClienteCreateForm
from src.services.cliente_service.data_service_dm import DataService

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

data_service = DataService()

@cliente_bp.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

@cliente_bp.route('/insert', methods=['GET', 'POST'])
def insert():
    form = ClienteCreateForm()

    # Inicializa las opciones de los SelectField
    try:
        departamentos = data_service.fetch_departamentos()
        form.departamento.choices = [('', 'Seleccione')] + [(depto, depto) for depto in departamentos]
    except Exception as e:
        return jsonify({'success': False, 'error': f"Error al cargar departamentos: {e}"}), 500

    # Vuelve a inicializar las opciones del municipio para asegurar que sean válidas en la validación del formulario
    if request.method == 'POST':
        departamento_seleccionado = form.departamento.data
        if departamento_seleccionado:
            try:
                municipios = data_service.fetch_municipios(departamento_seleccionado)
                form.municipio.choices = [('', 'Seleccione')] + [(muni, muni) for muni in municipios]
            except Exception as e:
              return jsonify({'success': False, 'error': f"Error al cargar municipios: {e}"}), 500

        if form.validate_on_submit():
            try:
                cliente = get_cliente_create_dic_from(form)
                print("Cliente creado:", cliente)  # Depuración: Verifica si se está creando el cliente correctamente

                #se registra el usuario
                email = form.correo.data 
                password = form.clave.data 

                user = auth.create_user_with_email_and_password(email, password)
                uid = user['localId']  # Obtener el UID del usuario

                print("El usuario es: ", user)
                print("UID del usuario: ", uid)
                
                # Agregar el UID al documento de Firestore
                id = uid
                
                Cliente_service.agregar_nuevo_cliente(cliente, id)
                return jsonify({'success': True}), 200
            except requests.exceptions.HTTPError as e:
                response_json = e.response.json()
                if response_json['error']['message'] == 'EMAIL_EXISTS':
                    return jsonify({'success': False, 'error': 'El correo electrónico ya está en uso'}), 400
                else:
                    return jsonify({'success': False, 'error': str(e)}), 400
            except Exception as e:
                return jsonify({'success': False, 'error': f"Error al guardar los datos: {e}"}), 500
        else:
            print(form.errors)
            return jsonify({'success': False, 'error': form.errors}), 400


@cliente_bp.route('/mostrar_registros_clientes', methods=['GET', 'POST'])
def mostrar_clientes():
    form = ClienteCreateForm()
    formUpdate = ClienteUpdateForm()
 
    departamentos = data_service.fetch_departamentos()
    form.departamento.choices = [('', 'Seleccione')] +  [(depto, depto) for depto in departamentos] 
    try:
        clientes = Cliente_service.obtener_registros_clientes()
        # Agregar municipios a cada cliente
        for cliente in clientes:
            if cliente.departamento:
                municipios = data_service.fetch_municipios(cliente.departamento)
                cliente.municipios = municipios
            else:
                cliente.municipios = []

    except Exception as e:
        flash(f"Error al obtener los clientes: {e}", "danger")
        clientes = []
    return render_template('/cliente/cliente_form.html', form=form, clientes=clientes, formUpdate=formUpdate)


@cliente_bp.route('/fetch_municipios', methods=['POST'])
def fetch_municipios():
    data = request.get_json()
    print(f"Datos recibidos: {data}")  # Debug: Verifica los datos recibidos
    departamento_seleccionado = data.get('departamento')
    if departamento_seleccionado:
        try:
            municipios = data_service.fetch_municipios(departamento_seleccionado)
            municipios_list = [{'value': muni, 'label': muni} for muni in municipios]
            return jsonify(municipios=municipios_list)
        except Exception as e:
            print(f"Error al obtener municipios: {e}")  # Debug: Mensaje de error
            return jsonify(error=str(e)), 500
    else:
        return jsonify(municipios=[])

@cliente_bp.route('/update/<id>', methods=['GET', 'POST'])
def postUpdate(id):
    formUpdate = ClienteUpdateForm()

    cliente = Cliente_service.obtener_cliente_por_id(id)
    success_messages = get_flashed_messages(category_filter=['success'])
    success = 'True' in success_messages  
    if request.method == 'GET':
        # Poblar el formulario con los datos del cliente en una solicitud GET
        formUpdate = ClienteUpdateForm(data=cliente)
        
    # Inicializa las opciones de los SelectField para GET y POST
    try:
        departamentos = data_service.fetch_departamentos()
        formUpdate.departamento.choices = [('', 'Seleccione')] + [(depto, depto) for depto in departamentos]

        departamento_seleccionado = cliente.get('departamento', None)
        if request.method == 'GET' and departamento_seleccionado:
            municipios = data_service.fetch_municipios(departamento_seleccionado)
            formUpdate.municipio.choices = [('', 'Seleccione')] + [(muni, muni) for muni in municipios]
    except Exception as e:
        print(f"Error al cargar departamentos o municipios: {e}")

    if request.method == 'POST':
        departamento_seleccionado = formUpdate.departamento.data
        if departamento_seleccionado:
            try:
                municipios = data_service.fetch_municipios(departamento_seleccionado)
                formUpdate.municipio.choices = [('', 'Seleccione')] + [(muni, muni) for muni in municipios]
            except Exception as e:
                print(f"Error al cargar municipios: {e}")

        if formUpdate.validate_on_submit():
            datosUpdate = get_cliente_update_dic_from(formUpdate)
            try:
                # Obtener instancia de auth
                firebase_auth = get_firebase_auth()

                update_data = {
                    'email': datosUpdate['correo']
                }

                # Solo agregar la contraseña si el campo no está vacío
                if formUpdate.clave.data:
                    update_data['password'] = formUpdate.clave.data

                # Actualizar datos en Firebase Authentication con Firebase Admin SDK
                print(f"Datos a actualizar: {datosUpdate}")
                user = firebase_auth.update_user(id, **update_data)
                print("El usuario", user)
                if user:
                    print("Usuario actualizado en Firebase Authentication")
                    Cliente_service.modificar_un_cliente(id, datosUpdate)
                    flash('True', 'success')  # Indicador de éxito usando flash
                    flash('Cliente actualizado correctamente', 'success')
                    return redirect(url_for('cliente_route.postUpdate', id=id))  # Redirigir al mismo formulario de edición
                else:
                    flash('Error al actualizar los datos de autenticación', 'danger')
            except firebase_admin.auth.EmailAlreadyExistsError:
                flash('El correo electrónico ya está en uso', 'danger')
            except firebase_admin.auth.UserNotFoundError:
                flash('Usuario no encontrado en Firebase Authentication', 'danger')
            except firebase_admin.auth.FirebaseError as e:
                flash(f'Error de Firebase: {e}', 'danger')
            except Exception as e:
                flash(f'Error al actualizar cliente: {e}', 'danger')
        else:
            print("Error en el formulario")
            print(formUpdate.errors)  # Imprimir los errores del formulario
            flash('Error en el formulario', "danger")
    
    print("Success antes de mandarlo para el template es: ", success)                
    return render_template('/cliente/update_client.html', formUpdate=formUpdate, cliente=cliente, success=success)


def get_cliente_create_dic_from(form):
    required_fields = ['tipo_identificacion', 'nombres', 'apellido', 'departamento', 'municipio', 'direccion', 'identificacion', 'experiencia', 'estudios_realizados', 'correo', 'clave', 'rol', 'celular']

    for field in required_fields:
        if not getattr(form, field).data:
            raise ValueError(f"El campo '{field}' no puede estar vacío")

    cliente_dict = {
        'tipo_identificacion': form.tipo_identificacion.data,
        'nombres': form.nombres.data,
        'apellido': form.apellido.data,
        'departamento': form.departamento.data,
        'municipio': form.municipio.data,
        'direccion': form.direccion.data,
        'identificacion': form.identificacion.data,
        'experiencia': form.experiencia.data,
        'estudios_realizados': form.estudios_realizados.data,
        'correo': form.correo.data,
        'clave': form.clave.data,
        'rol': form.rol.data,
        'celular': form.celular.data,
    }
    return cliente_dict



def get_cliente_update_dic_from(form):
    required_fields = ['tipo_identificacion', 'nombres', 'apellido', 'departamento', 'municipio', 'direccion', 'identificacion', 'experiencia', 'estudios_realizados', 'correo', 'rol', 'celular']

    for field in required_fields:
        if not getattr(form, field).data:
            raise ValueError(f"El campo '{field}' no puede estar vacío")

    cliente_dict = {
        'tipo_identificacion': form.tipo_identificacion.data,
        'nombres': form.nombres.data,
        'apellido': form.apellido.data,
        'departamento': form.departamento.data,
        'municipio': form.municipio.data,
        'direccion': form.direccion.data,
        'identificacion': form.identificacion.data,
        'experiencia': form.experiencia.data,
        'estudios_realizados': form.estudios_realizados.data,
        'correo': form.correo.data,
        'rol': form.rol.data,
        'celular': form.celular.data,
    }

    # Solo agregar la clave si está presente
    if form.clave.data:
        cliente_dict['clave'] = form.clave.data

    return cliente_dict


@cliente_bp.route('/delete/<id>', methods=['POST'])
def delete_cliente(id):
    try:

        firebase_auth = get_firebase_auth()

        firebase_auth.delete_user(id)
        print(f'Usuario {id} eliminado de Firebase Authentication')
        
        Cliente_service.eliminar_cliente(id)

        flash('Cliente eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar cliente: {e}', 'danger')
    return redirect(url_for('cliente_route.mostrar_clientes'))



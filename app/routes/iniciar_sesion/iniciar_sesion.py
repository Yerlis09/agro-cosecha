## importacion de flask ##
from flask import render_template, redirect, url_for, session, flash
from requests.exceptions import HTTPError


## importacion para la autenticación de usuarios ##
import pyrebase
from app.auth_token import firebaseConfig


## importacion de los blueprint ##
from . import login_bp


## importacion de los form ##
from src.validator_form.validator_login.login_form_wtf import LoginForm
from src.validator_form.validator_login.register_form import RegisterForm

## importacion del servicio de inicio de sesión ##
from src.services.iniciar_sesion.iniciar_sesion_service import InicioSesionService

from .permisos import PERMISSIONS

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


@login_bp.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    register_form = RegisterForm()
    context = {
        'login_form'    : login_form,
        'register_form' : register_form
    }
    return render_template('/iniciar_sesion/layout.html', **context)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        try:
            usuario = auth.sign_in_with_email_and_password(email, password)
            dataUsuarioValido = auth.get_account_info(usuario['idToken'])
            user_id = dataUsuarioValido['users'][0]['localId']
            
            user_info = InicioSesionService.obtener_info_usuario_por_id(user_id)
            if user_info:
                session['token'] = usuario['idToken']
                session['user_role'] = user_info.get('rol')
                session['user_id'] = user_info.get('document_id')
                session['permissions'] = PERMISSIONS.get(user_info.get('rol'), {})
                session['user_name'] = f"{user_info.get('nombres')} {user_info.get('apellido')}"
                
                
                print("El usuario en sesión es:", dataUsuarioValido)
                print("Permisos del usuario:", session['permissions'])
                # Redirigir según el rol del usuario
                role_redirects = {
                    'R-A1': 'main.zona_view',
                    'R-AG2': 'main.vuelo_view',
                    'R-R3': 'main.zona_view',
                    'R-AGR4': 'main.cuaderno_view',
                    'R-O5': 'main.cuaderno_view'
                }
                
                user_role = user_info.get('rol')
                if user_role in role_redirects:
                    return redirect(url_for(role_redirects[user_role]))
                else:
                    return redirect(url_for('main.get_dashboard'))

            flash("Usuario no encontrado en Firestore", 'error')
            return redirect(url_for('login.login'))

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            flash("Credenciales incorrectas", 'error')
            return redirect(url_for('login.login'))
        except Exception as e:
            print(f'Unexpected error occurred: {e}')
            flash("Error inesperado. Por favor, inténtalo de nuevo.", 'error')
            return redirect(url_for('login.login'))

    if login_form.errors:
        flash("Formulario inválido. Por favor, revisa los datos ingresados.", 'error')
    
    return render_template('iniciar_sesion/layout.html', login_form=login_form)


@login_bp.route('/logout')
def logout():
    session.pop('token', None)  
    session.pop('user_role', None)
    session.pop('user_id', None)
    return redirect(url_for('login.home'))
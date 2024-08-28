# permission_decorator.py
from flask import session, flash, redirect, url_for
from functools import wraps
from .permisos import PERMISSIONS

def permission_required(resource, *actions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = session.get('user_role')
            if role not in PERMISSIONS:
                flash('No tienes permiso para acceder a esta página.', 'error')
                return redirect(url_for('main.get_dashboard'))
            
            role_permissions = PERMISSIONS[role].get(resource, [])
            if not any(action in role_permissions for action in actions):
                flash('No tienes permiso para realizar esta acción.', 'error')
                return redirect(url_for('main.get_dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function
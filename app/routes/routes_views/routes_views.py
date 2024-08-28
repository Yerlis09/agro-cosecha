# views.py
from flask import render_template, redirect, url_for, session
from . import main_bp
from ..iniciar_sesion.decorators import permission_required, login_required

@main_bp.route('/get_dashboard')
@login_required
def get_dashboard():
    return redirect(url_for('zona_route.mostrar_zona'))

@main_bp.route('/cuaderno')
@login_required
@permission_required('bitacora', 'R', 'C', 'U', 'D')
def cuaderno_view():
    return redirect(url_for('bitacora_route.mostrar_bitacoras'))

@main_bp.route('/cliente')
@login_required
@permission_required('personas', 'R', 'C', 'U', 'D')
def cliente_view():
    return redirect(url_for('cliente_route.mostrar_clientes'))

@main_bp.route('/herramienta')
@login_required
@permission_required('herramienta', 'R', 'C', 'U', 'D')
def herramienta_view():
    return redirect(url_for('herramienta_route.mostrar_herramientas'))

@main_bp.route('/vuelo')
@login_required
@permission_required('plan_vuelo', 'R', 'C', 'U', 'D')
def vuelo_view():
    return redirect(url_for('plan_vuelo_route.mostrar_plan_vuelos'))

@main_bp.route('/zona')
@login_required
@permission_required('zonas', 'R', 'C', 'U', 'D')
def zona_view():
    return redirect(url_for('zona_route.mostrar_zona'))

@main_bp.route('/detectores')
@login_required
@permission_required('detectores', 'R', 'C', 'U', 'D')
def detectores_view():
    return redirect(url_for('detectores_route.mostrar_detectores'))

@main_bp.route('/inspecciones')
@login_required
@permission_required('inspecciones_campo', 'R', 'C', 'U', 'D')
def inspecciones_view():
    return redirect(url_for('ins_campo_route.mostrar_inspecciones_campo'))

@main_bp.route('/protocolos')
@login_required
@permission_required('protocolos', 'R', 'C', 'U', 'D')
def protocolos_view():
    return redirect(url_for('protocolo_route.mostrar_protocolos'))

@main_bp.route('/get_salir')
def salir_view():
    session.pop('token', None)
    session.pop('user_role', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('permissions', None)
    return redirect(url_for('login.login'))

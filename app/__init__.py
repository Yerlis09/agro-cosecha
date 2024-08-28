from flask import Flask, session, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect

from .routes.routes_views.routes_views import main_bp
from .routes.cliente.cliente_route import cliente_bp
from .routes.iniciar_sesion.iniciar_sesion import login_bp
from .routes.herramienta.herramienta_route import herramienta_bp
from .routes.planificacion_vuelo.planificacion_vuelo import plan_vuelo_bp
from .routes.zona.zona import zona_bp
from .routes.bitacora.bitacora_route import bitacora_bp
from .routes.detectores.detector_route import detectores_bp
from .routes.inspeccion_campo.inspeccion_campo_route import inspeccion_campo_bp
from .routes.protocolo.protocolo_route import protocolo_bp

#Importamos config
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf = CSRFProtect(app)

    # Registrar Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(herramienta_bp)
    app.register_blueprint(plan_vuelo_bp)
    app.register_blueprint(zona_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(detectores_bp)
    app.register_blueprint(inspeccion_campo_bp)
    app.register_blueprint(protocolo_bp)

    # Middleware para verificar la sesión en cada solicitud
    @app.before_request
    def check_session():
        if 'user_id' not in session and request.endpoint not in ['login.login', 'static']:
            flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('login.login'))

    return app
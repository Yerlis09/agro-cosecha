from flask import Blueprint

login_bp = Blueprint('login', __name__, url_prefix='/')

from . import iniciar_sesion
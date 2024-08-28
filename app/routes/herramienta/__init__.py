from flask import Blueprint

herramienta_bp = Blueprint('herramienta_route', __name__, url_prefix='/herramienta')

from . import herramienta_route
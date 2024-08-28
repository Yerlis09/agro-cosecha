from flask import Blueprint

protocolo_bp = Blueprint('protocolo_route', __name__, url_prefix='/protocolo')

from . import protocolo_route
from flask import Blueprint

bitacora_bp = Blueprint('bitacora_route', __name__, url_prefix='/bitacora')

from . import bitacora_route
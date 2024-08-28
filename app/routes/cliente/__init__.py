from flask import Blueprint

cliente_bp = Blueprint('cliente_route', __name__, url_prefix='/cliente')

from . import cliente_route
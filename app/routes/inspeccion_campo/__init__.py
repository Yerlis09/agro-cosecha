from flask import Blueprint

inspeccion_campo_bp = Blueprint('ins_campo_route', __name__, url_prefix='/inspeccion_campo')

from . import inspeccion_campo_route
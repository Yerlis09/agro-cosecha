from flask import Blueprint

plan_vuelo_bp = Blueprint('plan_vuelo_route', __name__, url_prefix='/plan_de_vuelo')

from . import planificacion_vuelo
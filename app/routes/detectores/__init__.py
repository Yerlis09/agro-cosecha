from flask import Blueprint

detectores_bp = Blueprint('detectores_route', __name__, url_prefix='/detectores')

from . import detector_route
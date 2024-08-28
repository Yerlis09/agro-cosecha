from flask import Blueprint

zona_bp = Blueprint('zona_route', __name__, url_prefix='/zona')

from . import zona
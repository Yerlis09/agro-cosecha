from flask import Blueprint

main_bp = Blueprint('main', __name__, url_prefix='/panel')

from . import routes_views
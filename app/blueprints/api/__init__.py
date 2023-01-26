from flask_cors import CORS

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix= '/api')
CORS(api)
from . import routes

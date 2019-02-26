from flask import Blueprint

json_api = Blueprint('json_api', __name__)

from . import api
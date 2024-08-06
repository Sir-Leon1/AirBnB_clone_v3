from flask import Blueprint, jsonify


app_views = Blueprint('app_view', __name__,
                      url_prefix='/api/v1')

from api.v1.views.index import *


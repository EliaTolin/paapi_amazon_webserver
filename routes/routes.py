from flask import Blueprint
from amazon_routes import amazon_route
from stats_routes import stats_route

base_api = Blueprint('base_api_v1', __name__, url_prefix='/api/v1/')

base_api.register_blueprint(amazon_route)
base_api.register_blueprint(stats_route)

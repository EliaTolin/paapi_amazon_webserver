from flask import Blueprint
from core.redis_manager import redis_manager
stats_route = Blueprint('stats_route', __name__, url_prefix='/stats')


@stats_route.route('/up_time_db')
def index():
    return redis_manager.time_created.strftime('%H:%M:%S')

from flask import Blueprint
from core.redis_manager import redis_manager
import constant.routes.stats_routes_constants as stats_routes

stats_route = Blueprint(stats_routes.name, __name__, url_prefix=stats_routes.url_prefix_route)


@stats_route.route(stats_routes.up_time_db_route)
def index():
    return redis_manager.time_created.strftime('%H:%M:%S')


@stats_route.route(stats_routes.status_db_route)
def status_db():
    if redis_manager.is_redis_available():
        return "ok", 200
    return "not_available", 500


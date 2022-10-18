from flask import Blueprint

stats_route = Blueprint('stats_route', __name__,url_prefix='/stats')

@stats_route.route('/')
def index():
    return "This is the index page STATS\n"
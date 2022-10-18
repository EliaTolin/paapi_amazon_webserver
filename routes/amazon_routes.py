from flask import Blueprint
from core.amazon_api import *

amazon_route = Blueprint('amazon_route', __name__,url_prefix='/pa_amazon')

@amazon_route.route('/')
def index():
    searchProduct('nintendo')
    return "This is the index page AMAZON\n"

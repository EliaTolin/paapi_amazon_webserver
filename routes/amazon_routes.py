from flask import Blueprint, request
from core.amazon_api import *
from core.redis_manager import redis_manager
import config


amazon_route = Blueprint('amazon_route', __name__, url_prefix='/pa_amazon')


@amazon_route.route('/get_category_offers', methods=['POST'])
def get_category_offers():
    category = request.values.get("category") or None
    if category is None:
        return "empty_category", 400

    if redis_manager.redis_db.exists(category):
        value = redis_manager.redis_db.get(category)
        return value
    else:
        redis_manager.redis_db.set(category, category)
        redis_manager.redis_db.expire(category, config.DATABASE_REFRESH_TIME_SECONDS)
        return "non exist"


@amazon_route.route('/search_product', methods=['POST'])
def search_product():
    wordlist = request.values.get("wordlist") or None
    if wordlist is None:
        return "empty_wordlist", 400

        # Get parameters
    actor = request.values.get("actor") or None
    artist = request.values.get("artist") or None
    author = request.values.get("author") or None
    brand = request.values.get("brand") or None
    title = request.values.get("title") or None
    max_price = request.values.get("max_price") or None
    min_price = request.values.get("min_price") or None
    min_saving_percent = request.values.get("min_saving_percent") or None
    min_reviews_rating = request.values.get("min_reviews_rating") or None
    search_index = request.values.get("search_index") or None
    sort = request.values.get("sort") or None

    list_products = search_products(keywords=wordlist, actor=actor, artist=artist, author=author, brand=brand,
                                    title=title, max_price=max_price, min_price=min_price,
                                    min_saving_percent=min_saving_percent, min_reviews_rating=min_reviews_rating,
                                    search_index=search_index, sort=sort)

    if len(list_products) == 0:
        return "empty_results", 204

    return list_products

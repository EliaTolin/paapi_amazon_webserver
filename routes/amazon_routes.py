from flask import Blueprint, request
from core.amazon_api import *
from models.exceptions.amazon_exception import *
from models.exceptions.redis_exception import *
import json


amazon_route = Blueprint('amazon_route', __name__, url_prefix='/pa_amazon')

amazonApiCore = AmazonApiCore()


def list_to_json(list_items):
    json_list = []
    for item in list_items:
        json_list.append(item.to_json().replace("\"", "\'"))
    return json_list


@amazon_route.route('/get_category_offers', methods=['POST'])
def get_category_offers_route():
    try:
        category = request.values.get("category", default=None)
        item_count = request.values.get("item_count", type=int) or None
        item_page = request.values.get("item_page", type=int) or None
        min_saving_percent = request.values.get("min_saving_percent", type=int) or None
        include_zero_offers = False
        if request.values.get("include_zero_offers", type=int, default=0) > 0:
            include_zero_offers = True
    except ValueError:
        return "wrong_type_parameter", 400

    if category is None:
        return "empty_category", 400
    try:
        list_products = amazonApiCore.get_category_offers(category, item_count=item_count, item_page=item_page,
                                                          min_saving_percent=min_saving_percent, include_zero_offers=include_zero_offers)

    except MissingParameterAmazonException:
        return "missing_parameter", 400

    except TooManyRequestAmazonException:
        return "too_many_request", 500

    except RedisConnectionException:
        return "redis_connection_error", 500

    if len(list_products) == 0:
        return "empty_results", 204

    return json.dumps(list_products)


@amazon_route.route('/search_product', methods=['POST'])
def search_product_route():
    wordlist = request.values.get("wordlist") or None
    if wordlist is None:
        return "empty_wordlist", 400

    # Get parameters
    try:
        actor = request.values.get("actor", default=None)
        artist = request.values.get("artist", default=None)
        author = request.values.get("author", default=None)
        brand = request.values.get("brand", default=None)
        title = request.values.get("title", default=None)
        max_price = request.values.get("max_price", type=int) or None
        min_price = request.values.get("min_price", type=int) or None
        min_saving_percent = request.values.get("min_saving_percent", type=int) or None
        min_reviews_rating = request.values.get("min_reviews_rating", type=int) or None
        search_index = request.values.get("search_index", default=None)
        sort = request.values.get("sort", default=None)
        item_count = request.values.get("item_count", type=int) or None
        item_page = request.values.get("item_page", type=int) or None
    except ValueError:
        return "wrong_type_parameter", 400
    try:
        list_products = amazonApiCore.search_products(keywords=wordlist, actor=actor, artist=artist, author=author,
                                                      brand=brand,
                                                      title=title, max_price=max_price, min_price=min_price,
                                                      min_saving_percent=min_saving_percent,
                                                      min_reviews_rating=min_reviews_rating,
                                                      search_index=search_index, sort=sort, item_page=item_page,
                                                      item_count=item_count)
    except MissingParameterAmazonException:
        return "missing_parameter", 400

    except TooManyRequestAmazonException:
        return "too_many_request", 500

    if len(list_products) == 0:
        return "empty_results", 204
    try:
        return list_products

    except ValueError:
        return "error_convert_json", 500

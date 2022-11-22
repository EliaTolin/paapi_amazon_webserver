from flask import Blueprint, request
from core.amazon_api import *
from models.exceptions.amazon_exception import *
from models.exceptions.redis_exception import *
import constant.params.amazon_params_constants as amazon_params
import constant.error_code_message_constants as error_code_message
import constant.routes.amazon_routes_constants as amazon_routes
import json

amazon_route = Blueprint(amazon_routes.name, __name__, url_prefix=amazon_routes.url_prefix_route)
amazonApiCore = AmazonApiCore()


def list_to_json(list_items):
    json_list = []
    for item in list_items:
        json_list.append(item.to_json().replace("\"", "\'"))
    return json_list


@amazon_route.route(amazon_routes.get_offers_route, methods=['POST'])
def get_category_offers_route():
    try:
        category = request.values.get(amazon_params.categoryParam, default=None)
        item_count = request.values.get(amazon_params.itemCountParam, type=int, default=10)
        item_page = request.values.get(amazon_params.itemPageParam, type=int, default=1)
        min_saving_percent = request.values.get(amazon_params.minSavingPercentParam, type=int) or None
        exclude_zero_offers = request.values.get(amazon_params.excludeZeroOffersParam, type=bool, default=False)
    except ValueError:
        return error_code_message.wrong_type_parameter, 400

    if category is None:
        return error_code_message.empty_category, 400
    try:
        list_products = amazonApiCore.get_category_offers(category, item_count=item_count, item_page=item_page,
                                                          min_saving_percent=min_saving_percent,
                                                          exclude_zero_offers=exclude_zero_offers)

    except CategoryNotExistException as e:
        return e.code_message, 400

    except MissingParameterAmazonException as e:
        return e.code_message, 400

    except TooManyRequestAmazonException as e:
        return e.code_message, 500

    except RedisConnectionException as e:
        return e.code_message, 500

    except InvalidArgumentAmazonException as e:
        return e.code_message, 400

    if len(list_products) == 0:
        if item_page > 1:
            return error_code_message.limit_reached_products, 204
        return error_code_message.empty_results, 204

    return json.dumps(list_products)


@amazon_route.route(amazon_routes.search_products_route, methods=['POST'])
def search_product_route():
    wordlist = request.values.get(amazon_params.wordlistParam) or None
    if wordlist is None:
        return error_code_message.empty_wordlist, 400

    # Get parameters
    try:
        actor = request.values.get(amazon_params.actorParam, default=None)
        artist = request.values.get(amazon_params.artistParam, default=None)
        author = request.values.get(amazon_params.authorParam, default=None)
        brand = request.values.get(amazon_params.brandParam, default=None)
        title = request.values.get(amazon_params.titleParam, default=None)
        max_price = request.values.get(amazon_params.maxPriceParam, type=int) or None
        min_price = request.values.get(amazon_params.minPriceParam, type=int) or None
        min_saving_percent = request.values.get(amazon_params.minSavingPercentParam, type=int) or None
        min_reviews_rating = request.values.get(amazon_params.minReviewsRatingParam, type=int) or None
        search_index = request.values.get(amazon_params.searchIndexParam, default=None)
        sort = request.values.get(amazon_params.sortParam, default=None)
        item_count = request.values.get(amazon_params.itemCountParam, type=int) or None
        item_page = request.values.get(amazon_params.itemPageParam, type=int) or None
    except ValueError:
        return error_code_message.wrong_type_parameter, 400
    try:
        list_products = amazonApiCore.search_products(keywords=wordlist, actor=actor, artist=artist, author=author,
                                                      brand=brand,
                                                      title=title, max_price=max_price, min_price=min_price,
                                                      min_saving_percent=min_saving_percent,
                                                      min_reviews_rating=min_reviews_rating,
                                                      search_index=search_index, sort=sort, item_page=item_page,
                                                      item_count=item_count)
    except MissingParameterAmazonException as e:
        return e.code_message, 400

    except TooManyRequestAmazonException as e:
        return e.code_message, 500

    if len(list_products) == 0:
        if item_page > 1:
            return error_code_message.limit_reached_products, 204
        return error_code_message.empty_results, 204

    try:
        json_list = []
        for el in list_products:
            json_list.append(el.to_json())
        return json.dumps(json_list)

    except ValueError:
        return error_code_message.error_convert_json, 500

from flask import Blueprint, request
from core.amazon_api import *
from helper.response_helper import make_response
from models.exceptions.amazon_exception import *
from models.exceptions.redis_exception import *
import constant.params.amazon_params_constants as amazon_params
import constant.exception.amazon_error_code_message as amazon_error_code_message
import constant.exception.generic_error_code_message as generic_error_code_message
import constant.routes.amazon_routes_constants as amazon_routes

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
        return make_response(status_code=generic_error_code_message.wrong_type_parameter), 400

    if category is None:
        return make_response(status_code=amazon_error_code_message.empty_category), 400
    try:
        list_products, limit_reached = amazonApiCore.get_category_offers(category, item_count=item_count,
                                                                         item_page=item_page,
                                                                         min_saving_percent=min_saving_percent,
                                                                         exclude_zero_offers=exclude_zero_offers)
        print(len(list_products))
    except InvalidArgumentAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except MissingParameterAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except TooManyRequestAmazonException as e:
        return make_response(status_code=e.code_message), 500

    except RedisConnectionException as e:
        return make_response(status_code=e.code_message), 500

    except CategoryNotExistException as e:
        return make_response(status_code=e.code_message), 400

    except ItemsNotFoundAmazonException as e:
        return make_response(status_code=e.code_message), 204

    if len(list_products) == 0:
        if item_page > 1:
            return make_response(status_code=amazon_error_code_message.limit_reached_products), 204
        return make_response(status_code=amazon_error_code_message.empty_results), 204
    try:
        if limit_reached:
            return make_response(data=list_products), 206
        return make_response(data=list_products), 200

    except ValueError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500
    except TypeError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500


@amazon_route.route(amazon_routes.search_products_route, methods=['POST'])
def search_product_route():
    wordlist = request.values.get(amazon_params.wordlistParam) or None
    if wordlist is None:
        return make_response(status_code=amazon_error_code_message.empty_wordlist), 400

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
        item_count = request.values.get(amazon_params.itemCountParam, type=int, default=10)
        item_page = request.values.get(amazon_params.itemPageParam, type=int, default=1) or None
        exclude_zero_price = request.values.get(amazon_params.excludeZeroPriceParam, type=bool, default=False)
        exclude_zero_offers = request.values.get(amazon_params.excludeZeroOffersParam, type=bool, default=False)
        only_prime_delivery = request.values.get(amazon_params.only_prime_delivery, type=bool, default=False)

    except ValueError:
        return make_response(status_code=generic_error_code_message.wrong_type_parameter), 400

    except TypeError:
        return make_response(status_code=generic_error_code_message.wrong_type_parameter), 400

    try:
        list_products, limit_reached = amazonApiCore.search_products(keywords=wordlist, actor=actor, artist=artist,
                                                                     author=author,
                                                                     brand=brand,
                                                                     title=title, max_price=max_price,
                                                                     min_price=min_price,
                                                                     min_saving_percent=min_saving_percent,
                                                                     min_reviews_rating=min_reviews_rating,
                                                                     search_index=search_index, sort=sort,
                                                                     item_page=item_page,
                                                                     item_count=item_count,
                                                                     exclude_zero_price=exclude_zero_price,
                                                                     exclude_zero_offers=exclude_zero_offers,
                                                                     only_prime_delivery=only_prime_delivery)
    except MissingParameterAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except TooManyRequestAmazonException as e:
        return make_response(status_code=e.code_message), 500
    
    except RedisConnectionException as e:
        return make_response(status_code=e.code_message), 500

    except CategoryNotExistException as e:
        return make_response(status_code=e.code_message), 400
    
    except ItemsNotFoundAmazonException as e:
        return make_response(status_code=e.code_message), 204
    
    if len(list_products) == 0:
        if item_page > 1:
            return make_response(status_code=amazon_error_code_message.limit_reached_products), 204
        return make_response(status_code=amazon_error_code_message.empty_results), 204

    try:
        products_json_list = []
        for el in list_products:
            products_json_list.append(el.to_json())
        if limit_reached:
            return make_response(data=products_json_list, status_code=generic_error_code_message.no_error), 206
        return make_response(data=products_json_list, status_code=generic_error_code_message.no_error), 200

    except ValueError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500

    except TypeError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500


@amazon_route.route(amazon_routes.add_category_preference, methods=['POST'])
def add_category_preference():
    list_search_category = request.values.getlist(amazon_params.list_category_preference)
    for category in list_search_category:
        redis_manager.redis_db.incr(category+database_constants.key_suffix_preference)
    return make_response(status_code=generic_error_code_message.no_error),200

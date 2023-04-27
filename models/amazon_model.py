from amazon_paapi.models import Item
import jsonpickle

from models.exceptions.amazon_exception import *


class AmazonItem:
    def __init__(self, product: Item):
        if product.asin is not None:
            self.product_asin = product.asin
        else:
            self.product_asin = None

        if product.item_info.title.display_value is not None:
            self.title = product.item_info.title.display_value
        else:
            self.title = None

        if product.item_info.product_info is not None:
            if product.item_info.product_info.color is not None:
                self.product_info_color = product.item_info.product_info.color.display_value
        else:
            self.product_info_color = None

        if product.offers.listings[0] is not None and product.offers.listings[0].price is not None:

            if product.offers.listings[0].price.amount is not None:
                self.price_actual = product.offers.listings[0].price.amount
            else:
                self.price_actual = None

            if product.offers.listings[0].price.currency is not None:
                self.price_currency = product.offers.listings[0].price.currency
            else:
                self.price_currency = None

            if product.offers.listings[0].price.savings is not None:
                if product.offers.listings[0].price.savings.amount is not None:
                    self.price_saving_amount = product.offers.listings[0].price.savings.amount
                else:
                    self.price_saving_amount = None

                if product.offers.listings[0].price.savings.percentage is not None:
                    self.price_saving_amount_percentage = product.offers.listings[0].price.savings.percentage
                else:
                    self.price_saving_amount_percentage = None
            else:
                self.price_saving_amount = None
                self.price_saving_amount_percentage = None
        else:
            self.price_actual = None
            self.price_currency = None
            self.price_saving_amount = None
            self.price_saving_amount_percentage = None

        if product.offers.listings[0].saving_basis is not None:
            if product.offers.listings[0].saving_basis.amount is not None:
                self.price_base = product.offers.listings[0].saving_basis.amount
            else:
                self.price_base = None
            if product.offers.listings[0].delivery_info is not None:
                self.prime_delivery = product.offers.listings[0].delivery_info.is_prime_eligible
                self.amazon_fulfilled = product.offers.listings[0].delivery_info.is_amazon_fulfilled
            else:
                self.amazon_fulfilled = None
                self.prime_delivery = None
        else:
            self.price_base = None
            self.prime_delivery = None

        if product.offers.summaries[0] is not None:
            if product.offers.summaries[0].highest_price is not None:
                self.price_highest = product.offers.summaries[0].highest_price.amount
            else:
                self.price_highest = None
            if product.offers.summaries[0].lowest_price is not None:
                self.price_lowest = product.offers.summaries[0].lowest_price.amount
            else:
                self.price_lowest = None
        else:
            self.price_highest = None
            self.price_lowest = None

        if product.score is not None:
            self.score = product.score
        else:
            self.score = None

        if product.images.primary.large is not None:
            self.images_large = product.images.primary.large
        else:
            self.images_large = None

        if product.images.primary.medium is not None:
            self.images_medium = product.images.primary.medium
        else:
            self.images_medium = None

        if product.images.primary.small is not None:
            self.images_small = product.images.primary.small
        else:
            self.images_small = None

        if product.detail_page_url is not None:
            self.product_url = product.detail_page_url
            self.share_url = product.detail_page_url
        else:
            raise UrlNotDefinedAmazonException

    def to_json(self):
        return jsonpickle.encode(self, unpicklable=False)
        # object_json = json.dumps(self, default=lambda o: o.__dict__)
        # return object_json.replace("\"","\'")

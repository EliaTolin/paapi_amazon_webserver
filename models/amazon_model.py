from amazon_paapi.models import Item
import json

from models.amazon_exception import *


# print(item.images.primary.large.url)  # Primary image url
# print(item.offers.listings[0].price.amount)  # Current price

class AmazonItem:
    def __init__(self, product: Item):
        if product.asin is not None:
            self.product_asin = product.asin

        if product.item_info.title.display_value is not None:
            self.title = product.item_info.title.display_value

        if product.item_info.product_info is not None:
            if product.item_info.product_info.color is not None:
                self.product_info_color = product.item_info.product_info.color.display_value

        if product.offers.listings[0].price.amount is not None:
            self.price_actual = product.offers.listings[0].price.amount

        if product.offers.listings[0].price.currency is not None:
            self.price_currency = product.offers.listings[0].price.currency

        if product.offers.listings[0].price.savings is not None:
            if product.offers.listings[0].price.savings.amount is not None:
                self.price_saving_amount = product.offers.listings[0].price.savings.amount
            if product.offers.listings[0].price.savings.percentage is not None:
                self.price_saving_amount_percentage = product.offers.listings[0].price.savings.percentage

        if product.offers.listings[0].saving_basis is not None:
            if product.offers.listings[0].saving_basis.amount is not None:
                self.price_base = product.offers.listings[0].saving_basis.amount
            if product.offers.listings[0].delivery_info is not None:
                self.prime_delivery = product.offers.listings[0].delivery_info.is_prime_eligible
        if product.offers.summaries[0] is not None:
            if product.offers.summaries[0].highest_price is not None:
                self.price_highest = product.offers.summaries[0].highest_price.amount
            if product.offers.summaries[0].lowest_price is not None:
                self.price_lowest = product.offers.summaries[0].lowest_price.amount

        if product.score is not None:
            self.score = product.score

        if product.images.primary.large is not None:
            self.images_large = product.images.primary.large
        if product.images.primary.medium is not None:
            self.images_medium = product.images.primary.medium
        if product.images.primary.small is not None:
            self.images_small = product.images.primary.small

        if product.detail_page_url is not None:
            self.product_url = product.detail_page_url
        else:
            raise UrlNotDefinedAmazonException

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

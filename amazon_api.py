from amazon_paapi import AmazonApi
from config import *

amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, 'IT')


def get_product_by_name(name):
    search_results = amazon.search_items(keywords=name)
    for item in search_results.items:
        print(item.images.primary.large.url)  # Primary image url
        print(item.offers.listings[0].price.amount)  # Current price
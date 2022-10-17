# This is a sample Python script.
import amazon_paapi
from amazon_paapi import AmazonApi

from config import *

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, 'IT')

def get_product_by_name(name):
    search_results = amazon.search_items(keywords=name)
    for item in search_results.items:
        print(item.images.primary.large.url)  # Primary image url
        print(item.offers.listings[0].price.amount)  # Current price


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_product_by_name('nintendo')

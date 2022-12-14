from config import *
from datetime import datetime
from amazon_paapi import AmazonApi


class AmazonManager:
    def __init__(self):
        self.amazon_api = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, AMAZON_COUNTRY,
                                    throttling=THROTTLING_SECONDS)
        self.time_created = datetime.now().time()


amazon_manager = AmazonManager()

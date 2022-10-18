from amazon_paapi import Item
# print(item.images.primary.large.url)  # Primary image url
# print(item.offers.listings[0].price.amount)  # Current price
        
class AmazonItem: 
    def __init__(self,product : Item):
        self.name = product.item.images.primary.large.url
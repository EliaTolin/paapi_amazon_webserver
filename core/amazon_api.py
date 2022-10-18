from amazon_paapi import AmazonApi
from config import *
from models.amazon_model import AmazonItem
amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, 'IT')

# (method) search_items: (item_count: int = None, item_page: int = None, actor: str = None, artist: str = None, author: str = None, brand: str = None, 
# keywords: str = None, title: str = None, availability: Availability = None, browse_node_id: str = None, condition: Condition = None,
# currency_of_preference: str = None, delivery_flags: List[str] = None, languages_of_preference: List[str] = None, merchant: Merchant = None, 
# max_price: int = None, min_price: int = None, min_saving_percent: int = None, min_reviews_rating: int = None, search_index: str = None, 
# sort_by: SortBy = None, **kwargs: Any) -> SearchResult

def searchProduct(keywords, actor: str = None, artist: str = None, author: str = None, brand: str = None,title:str = None,
                  max_price: int = None, min_price: int = None, min_saving_percent: int = None, min_reviews_rating: int = None):
    search_results = amazon.search_items(keywords=keywords,
        actor=actor,artist = artist, author=author, brand=brand,title=title,max_price=max_price,min_price=min_price,min_saving_percent=min_saving_percent,
        min_reviews_rating=min_reviews_rating)
    for item in search_results.items:
        itemA = AmazonItem(item)
        print(item.images.primary.large.url)  # Primary image url
        print(item.offers.listings[0].price.amount)  # Current price
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooktopiaItem(scrapy.Item):
    title_of_book = scrapy.Field()
    author = scrapy.Field()
    book_type = scrapy.Field()
    original_price = scrapy.Field()
    discounted_price = scrapy.Field()
    ISBN_10 = scrapy.Field()
    published_date = scrapy.Field()
    publisher = scrapy.Field()
    no_of_pages = scrapy.Field()
    pass

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlcaptureItem(scrapy.Item):
    # define the fields for your item here like:
    urls = scrapy.Field()
    layer = scrapy.Field()
    category = scrapy.Field()
    indomain = scrapy.Field()

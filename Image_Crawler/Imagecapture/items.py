# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ResearchItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class ImageItem(scrapy.Item):
    image_name = scrapy.Field()
    image_urls = scrapy.Field()
    relative_path = scrapy.Field()
    layer = scrapy.Field()
    category = scrapy.Field()
    indomain = scrapy.Field()
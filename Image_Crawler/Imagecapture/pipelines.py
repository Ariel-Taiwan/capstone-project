# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
import scrapy


class CustomImagesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_urls'])

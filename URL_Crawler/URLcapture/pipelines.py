# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
import pymongo
import os
class CsvPipeline:
    collection = 'links'

    @classmethod 
    def from_crawler(cls, crawler): 
        output = os.path.abspath("./output") + '/urls/' + str(crawler.settings.get('output'))
        mongodb_uri = crawler.settings.get('MONGODB_URI'),
        mongodb_db = crawler.settings.get('MONGODB_DATABASE', 'items')
        layer = crawler.settings.get('layer')
        category = crawler.settings.get('category')
        argument_list = [output, mongodb_uri, mongodb_db, layer, category]

        return cls(argument_list) 

    def __init__(self, argument_list):
        # Open files
        self.file = open(argument_list[0], 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='big5')
        self.exporter.start_exporting()
        
        self.mongodb_uri = argument_list[1]
        self.mongodb_db = argument_list[2]
        self.layer = argument_list[3]
        self.category = argument_list[4]

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # self.db[self.collection].delete_many({})      # Clear the content of collections

    def process_item(self, item, spider):
        item['layer'] = self.layer
        item['category'] = self.category
        data = dict(item)
        try:
            # insert into new collection
            self.db[self.collection].insert_one(data)
        except pymongo.errors.DuplicateKeyError:
            # skip document because it already exists in new collection
            pass
        else:
            self.exporter.export_item(item)
        
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        self.client.close()

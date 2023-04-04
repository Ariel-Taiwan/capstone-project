import scrapy
import os
import hashlib
import pymongo
import mimetypes
import pandas as pd
from Imagecapture.items import ImageItem
from scrapy.utils.python import to_bytes


class ExampleSpider(scrapy.Spider):
    name = 'example'

    input_urls_directory = os.path.abspath("./input/urls") + '/'
    start_urls = []
    col_list = ["category", "layer", "indomain", "urls"] 
    relative_output_images_path = ''
    mongodb_uri = ''
    mongodb_db = ''
    collection = 'images'

    def __init__(self, *args, **kwargs): 
        super(ExampleSpider, self).__init__(*args, **kwargs) 
        self.input_urls_directory += self.input
        self.relative_output_images_path = '/cat' + str(self.category) + '/' + self.parseLayer(self.layer) + '/'

        self.mongodb_uri = self.MONGODB_URI
        self.mongodb_db = self.MONGODB_DATABASE

        # Read a URL file
        df = pd.read_csv(self.input_urls_directory, usecols = self.col_list, encoding= 'unicode_escape')
        self.start_urls = df["urls"].tolist()

        # Connect and open MongoDB
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        
        
    def start_request(self):
        for url in self.start_urls:
            yield Request(url = url, callback = self.parse)


    def parse(self, response):
        domain = self.getDomain(response.url)

        if response.status == 200:
            rel_img_urls = response.xpath("//img/@src").getall()

            for rel_img_url in rel_img_urls:
                complet_url = response.urljoin(rel_img_url)

                if rel_img_url.startswith('http') or rel_img_url.startswith('https'):
                    target_domain = self.getDomain(complet_url)
                # If the url is DATA URI, consider it is in domain
                else:   
                    target_domain = domain

                # Get image hash name
                # Reference from source code: https://docs.scrapy.org/en/latest/_modules/scrapy/pipelines/files.html#FilesPipeline.file_path
                image_hash_name = hashlib.sha1(to_bytes(complet_url)).hexdigest()
                image_ext = os.path.splitext(complet_url)[1]
                
                if image_ext not in mimetypes.types_map:
                    image_ext = ''
                    media_type = mimetypes.guess_type(complet_url)[0]
                    if media_type:
                        image_ext = mimetypes.guess_extension(media_type)

                image_name = image_hash_name + image_ext
                

                item = ImageItem()
                item['image_urls'] = complet_url
                item['layer'] = self.layer
                item['category'] = self.category
                item['relative_path'] = self.relative_output_images_path

                # Compare the target url is in the same domain with the request url
                if domain == target_domain:
                    item['indomain'] = 1
                else:
                    item['indomain'] = 0

                item['image_name'] = image_name
                
                data = dict(item)

                try:
                    # insert into new collection
                    self.db[self.collection].insert_one(data)
                except pymongo.errors.DuplicateKeyError:
                    # skip document because it already exists in new collection
                    pass
                except:
                    raise
                else:
                    yield item


    def close_spider(self, spider):
        self.client.close()


    def getDomain(self, url):
        request_url = url.split('/')
        print(request_url)
        domain = request_url[2]
        return domain
 
    def parseLayer(self, pattern):
        if pattern == '0':
            return "root"
        elif pattern ==  '1':
            return "first"
        elif pattern ==  '2':
            return "second"
        else:
            return "third"
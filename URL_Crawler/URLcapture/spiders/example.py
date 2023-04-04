import scrapy
from scrapy import Request
from URLcapture.items import UrlcaptureItem
import pandas as pd
import os

class ExampleSpider(scrapy.Spider):
    name = 'example'
    input_urls_directory = os.path.abspath("./input") + '/urls/'
    start_urls = []
    col_list = ["category", "layer", "indomain", "urls"]

    def __init__(self, input = None, *args, **kwargs): 
        super(ExampleSpider, self).__init__(*args, **kwargs) 
        self.input_urls_directory += input

        df = pd.read_csv(self.input_urls_directory, usecols = self.col_list, encoding= 'unicode_escape')
        self.start_urls = df["urls"].tolist()
        

    def start_request(self):
        for url in self.start_urls:
            Request(url = url, callback = self.parse)

    def parse(self, response):
    
        domain = self.getDomain(response.url)

        if response.status == 200:
            urls = response.xpath("//a/@href").getall()

            for url in urls:
                print("!!!!!!")
                # String starts with / or http or https can add to list
                if url.startswith('/') or url.startswith('http') or url.startswith('https'):
                    complet_url = response.urljoin(url)
                    target_domain = self.getDomain(complet_url)
                    
                    item = UrlcaptureItem()
                    item['urls'] = complet_url

                    # Compare the target url is in the same domain with the request url
                    if domain == target_domain:
                        item['indomain'] = 1
                    else:
                        item['indomain'] = 0
                    
                    yield item

    def getDomain(self, url):
        request_url = url.split('/')
        domain = request_url[2]
        return domain
 

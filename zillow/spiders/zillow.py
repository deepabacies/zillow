from __future__ import absolute_import, unicode_literals, print_function

import re

import json

from babel.numbers import parse_number
import scrapy

#from scraper.items import HomeListing
from zillow.items import HomeListing

BASE_URL = 'http://zillow.com'

SOLD_PROPERTURL = '/homes/recently_sold'

SOLD_PROPERTY_PARAM = "/4099_rid/globalrelevanceex_sort/39.269474,-84.28402,38.972755,-84.719353_rect/10_zm/"

class ZillowScraper(scrapy.Spider):
    name = 'zillow'

    def __init__(self, *args, **kwargs):
        super(ZillowScraper, self).__init__(*args, **kwargs)
        city = 'CINCINNATI' #kwargs.get('city')
        state = 'OH' #kwargs.get('state')
        if not city:
            raise ValueError('city parameter not defined')
        if not state:
            raise ValueError('state parameter not defined')
        self.city = city
        self.state = state

    def start_requests(self):
        url = BASE_URL + SOLD_PROPERTURL
        city = self.city
        state = self.state
        if city is not None and state is not None:
            url = url + '/' + city + '-' + state           
            url = url + SOLD_PROPERTY_PARAM
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        listing = {} #HomeListing()
        listing['mytest'] = "testzillow"
        #listing['title'] = response.xpath('//title/text()').extract_first()
        mylist = []
        i = 1
        for atag in response.xpath('//div[@id="search-results"]/ul/li'):
            mydict = {}
            for x in atag.xpath('.//article/div[1]'):  
                # Tag A
                street = x.xpath('.//span[1]/span[1]/text()').extract_first()
                city = x.xpath('.//span[1]/span[2]/text()').extract_first()
                state = x.xpath('.//span[1]/span[3]/text()').extract_first()
                postalcode = x.xpath('.//span[1]/span[4]/text()').extract_first()
                mydict['address'] = street+' '+city+' '+state+' '+postalcode
                mydict['sold'] = x.xpath('.//div[1]/h4/span/text()').extract_first()
                mydict['path'] = BASE_URL + x.xpath('.//a[1]/@href').extract_first()
            mylist.append(mydict)
            i = i + 1            
        listing['details'] = mylist
        listing['propertycounter'] = str(i)
        print(json.dumps(listing))
    
# scrapy crawl zillow -o zillow.json

# Tag A................
# <div id=search-results><ul><li>....
#
#...<article><div>..</article></div> <article><div>..</article></div> ......
#..... <article><div> <span[1]>property address</span>
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request


from azulcrawler.items import AzulcrawlerItem

import urlparse
import re


class RestaurantSpider(BaseSpider):
    name = 'categories'
    allowed_domains = ['yelp.com']
    start_urls = ['http://www.yelp.com/c/austin/restaurants']    #Root urls for spider

    def parse(self, response):
        l = XPathItemLoader(item = AzulcrawlerItem(), response = response)
        l.add_xpath('categories', '//div[@id = "subcategories-list"]/div/ul/li/ul[@class = "column-set"]/li/a/text()')
        return l.load_item()

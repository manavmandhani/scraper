from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request


from crawler.items import CrawlerItem

import urlparse
import re


class RestaurantSpider(BaseSpider):
    name = 'crawlyelp'
    allowed_domains = ['yelp.com']
    start_urls = ['http://www.yelp.com/c/austin/restaurants']    #Root urls for spider
    
#Returns a list of all categories of restaurants within a particular city
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        total_category_list = hxs.select('//div[@id = "subcategories-list"]/div/ul/li/ul[@class = "column-set"]/li/a/@href').extract()
        crawl_category_list = total_category_list[0:2]
        for nextcategory in crawl_category_list:
            yield Request(urlparse.urljoin('http://yelp.com', nextcategory), callback = self.parse_restaurant)

#Moves from a mosaic display to a list display
    def parse_restaurant(self, response):
        hxs = HtmlXPathSelector(response)
        next_restaurant = hxs.select('//a[@class = "see-more-link link-pill"]/@href').extract()
        if next_restaurant:
            yield Request(urlparse.urljoin('http://yelp.com', next_restaurant[0]) , callback = self.parse_list)
        else:
            yield Request(urlparse.urljoin('http://yelp.com', response.url), callback = self.parse_page)

#Extract a list of all the pages of restaurants
    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)
        page_list = hxs.select('//a[@class = "page-option available-number"]/@href').extract()
        for nextpage in page_list:
            yield Request(urlparse.urljoin('http://yelp.com', nextpage), callback = self.parse_page)

#Extract a list of all restaurants within a page
    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//span[@class = "indexed-biz-name"]/a/@href').extract():
            yield Request(urlparse.urljoin('http://yelp.com', url), callback = self.parse_item)

#Scrapes data within a page and assigns it to the Item fields
    def parse_item(self, response):
        l = XPathItemLoader(item = AzulcrawlerItem(), response=response)
        l.add_xpath('name', '//h1/text()')
        l.add_xpath('number', '//span[@id = "bizPhone"]/text()')
        l.add_xpath('categories', '//span[@itemprop = "title"]/text()')
        l.add_xpath('address', '//span[@itemprop="streetAddress"]/text()')
        l.add_xpath('address', '//span[@itemprop="addressLocality"]/text()')
        l.add_xpath('address', '//span[@itemprop="addressRegion"]/text()')
        l.add_xpath('address', '//span[@itemprop="postalCode"]/text()')
        l.add_xpath('rating', '//div[@itemprop="aggregateRating"]/div/meta/@content')
        l.add_xpath('price_range', '//span[@id="price_tip"]/text()')
        l.add_xpath('url', '//div[@id = "bizUrl"]/a/text()')
        l.add_xpath('hours', '//p[@class = "hours"]/text()')
        return l.load_item()


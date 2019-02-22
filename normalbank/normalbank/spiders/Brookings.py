# -*- coding: utf-8 -*-
import scrapy


class BrookingsSpider(scrapy.Spider):
    name = 'Brookings'
    allowed_domains = ['brookings.edu']
    start_urls = ['https://www.brooking'
                  's.edu/']

    def parse(self, response):
        pass

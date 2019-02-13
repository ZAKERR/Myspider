# -*- coding: utf-8 -*-
import scrapy


class BrookingsSpider(scrapy.Spider):
    name = 'Brookings'
    allowed_domains = ['brookings.edu']
    start_urls = ['https://www.brookings.edu/']

    def make_requests_from_url(self):

    def parse(self, response):
        pass

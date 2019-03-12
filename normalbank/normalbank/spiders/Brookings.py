# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem
from normalbank.spiders import get_proxy_pool
HEADERS_NOR = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
class BrookingsSpider(scrapy.Spider):
    name = 'brookings'
    allowed_domains = ['brookings.edu']

    def start_requests(self):
        URL = 'https://www.brookings.edu/search/?post_type=post&post_type=bpea-article&post_type=research&post_type=testimony&orderby=date'
        yield scrapy.Request(url = URL ,headers= HEADERS_NOR,callback = self.parse_index)

    def parse_index(self, response):
        tds = response.xpath("//div[@class='list-content']/article")
        for td in tds:
            article = NormalbankItem()
            article["link"] = td.xpath(".//div[@class='image-wrapper']/a/@href").extract_first()
            article["title"] = td.xpath(".//h4//text()").extract_first()
            article["push_date"] = td.xpath(".//time//text()").extract_first()
            article['text'] = 'tag-end'
            yield article


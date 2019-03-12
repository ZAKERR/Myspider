# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem

HEADERS_NOR = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
class BruegelSpider(scrapy.Spider):
    name = 'bruegel'
    allowed_domains = ['bruegel.org']

    def start_requests(self):
        url = 'http://bruegel.org/publications/'
        yield scrapy.Request(url=url,headers=HEADERS_NOR,callback=self.parse_main)
        next_url = 'http://bruegel.org/blog/'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_main)

    def parse_main(self, response):
        tds= response.xpath("//body/a")[0:-1]
        item = NormalbankItem()
        for td in tds:
            item["title"] = td.xpath("./div[1]/div[4]/h2/text()").extract_first()
            item["text"] = td.xpath("./div[1]/div[4]/p/text()").extract_first()
            item['link'] = td.xpath("./@href").extract_first()
            item["push_date"] = td.xpath("./div[1]/div[4]/div/span[3]/text()").extract_first()
            yield item

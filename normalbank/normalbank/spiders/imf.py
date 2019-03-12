# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem

HEADERS_NOR = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

class ImfSpider(scrapy.Spider):
    name = 'imf'
    allowed_domains = ['imf.org/']

    def start_requests(self):
        url = 'https://www.imf.org/external/what/whatsnewenglish/what.aspx?Page=1'
        yield scrapy.Request(url = url ,headers=HEADERS_NOR,callback=self.parse_index)

    def parse_index(self, response):
        h4 = response.xpath("//*[@id='content-main']/h4")
        p = response.xpath("//*[@id='content-main']/p")
        for (i, t) in zip(h4, p):
            item = NormalbankItem()
            item["title"] = i.xpath("./a/text()").extract_first()
            item["push_date"] = t.xpath("./span/text()").extract_first()
            item['link'] = i.xpath(".//@href").extract_first()
            item['text'] = 'tag-end'
            yield item

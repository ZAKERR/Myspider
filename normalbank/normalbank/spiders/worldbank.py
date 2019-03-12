# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem
import json

HEADERS_NOR = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

class WorldbankSpider(scrapy.Spider):
    name = 'worldbank'
    allowed_domains = ['openknowledge.worldbank.org',
                       'worldbank.org']

    def start_requests(self):
        url = 'http://search.worldbank.org/api/v2/news?format=json&rows=20&fct=displayconttype_exact,topic_exact,lang_exact,count_exact,countcode_exact,admreg_exact&src=cq55&apilang=en&lang_exact=English&count_exact=China'
        yield scrapy.Request(url = url ,headers=HEADERS_NOR,callback=self.parse_all)
        next_url = 'https://openknowledge.worldbank.org/recent-submissions'
        yield scrapy.Request(url = url,headers=HEADERS_NOR,callback=self.parse_report)

    def parse_report(self,response):
        tds = response.xpath("//li[@class='ds-artifact-item even'] | //li[@class='ds-artifact-item odd']")
        for td in tds:
            item = NormalbankItem()
            item["title"] = td.xpath(".//h4/a/text()").extract_first()
            item["name"] = td.xpath(".//div[@class='content author-info']/span/a/text()").extract_first()
            item["text"] = td.xpath(".//div[@class='artifact-info hidden-md hidden-lg']/span/a/text()").extract_first()
            item['link'] = td.xpath(".//span/a/@href").extract_first()
            yield item

    def parse_all(self, response):
        text = response.body.decode("utf-8")
        tds = json.loads(text)['documents']
        for key in tds.keys():
            if tds[key].get('url') != None:
                item = NormalbankItem()
                item['link'] = tds[key]['url']
                item['title'] = tds[key]['title']['cdata!']
                item['text'] = tds[key]['descr']['cdata!']
                item['push_date'] = tds[key]['lnchdt']
                yield item

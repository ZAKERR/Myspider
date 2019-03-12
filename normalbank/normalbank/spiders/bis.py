# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem

HEADERS_NOR = {
    'Host':'www.bis.org',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

class BisSpider(scrapy.Spider):
    name = 'bis'
    allowed_domains = ['bis.org']

    def start_requests(self):
        url = 'https://www.bis.org/list/research/index.htm'
        yield scrapy.Request(url = url,headers=HEADERS_NOR,callback=self.parse_index)
        next_url = 'https://www.bis.org/doclist/annualeconomicreports.htm'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_index)
        next_url = 'https://www.bis.org/doclist/bispapers.htm'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_index)
        next_url = 'https://www.bis.org/doclist/wpapers.htm'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_index)
        next_url = 'https://www.bis.org/fsi/fsiinsights.htm'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_index)
        next_url = 'https://www.bis.org/fsi/fsisummaries.htm'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_fsi)
        next_url = 'https://www.bis.org/doclist/bcbs/publications.htm'
        yield scrapy.Request(url=next_url,headers=HEADERS_NOR,callback=self.parse_index)
        next_url = 'https://www.bis.org/list/bcbs_sp/index.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/list/cgfs/index.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/list/cpmi/index.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/list/mktc/index.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/doclist/aoresearchpubs.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/list/press_releases/index.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/doclist/mgmtspeeches.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/list/bcbs_sp/index.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)
        next_url = 'https://www.bis.org/doclist/cbspeeches.htm'
        yield scrapy.Request(url=next_url, headers=HEADERS_NOR, callback=self.parse_index)


    def parse_index(self, response):
        tds = response.xpath("//tr[@class='item even'] | //tr[@class='item odd']")
        for td in tds:
            item = NormalbankItem()
            item["title"] = td.xpath("./td[2]/div[1]/a/text()").extract_first()
            item["push_date"] = td.xpath("./td[1]/text()").extract_first().strip()
            item['link'] = td.xpath(".//a/@href").extract_first()
            item["text"] = "tag-end"
            yield item

    def parse_fsi(self,response):
        tds = response.xpath("//tbody/tr")
        for td in tds:
            item = NormalbankItem()
            item["title"] = td.xpath("./td[2]/a/text()").extract_first()
            item["push_date"] = td.xpath("./td[1]/text()").extract_first().strip()
            item["link"] = td.xpath(".//a/@href").extract_first()
            item['text'] = 'tag-end'
            yield item


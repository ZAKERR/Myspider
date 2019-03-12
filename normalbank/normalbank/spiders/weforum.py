# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem
HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host':'www.weforum.org',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

BASE_URL = "https://www.weforum.org"
class WeforumSpider(scrapy.Spider):
    name = 'weforum'
    allowed_domains = ['weforum.org']

    def start_requests(self):
        next_url = 'https://www.weforum.org/agenda/archive'
        yield scrapy.Request(url = next_url,headers=HEADERS,callback=self.parse_agenda)
        next_url = 'https://www.weforum.org/whitepapers'
        yield scrapy.Request(url = next_url,headers = HEADERS,callback=self.parse_whitepapers)
        next_url = 'https://www.weforum.org/reports'
        yield scrapy.Request(url = next_url,headers=HEADERS,callback=self.parse_whitepapers)


    def parse_agenda(self,response):
        tds = response.xpath("//div[@class='columns']/div/div/article")
        for td in tds:
            article = NormalbankItem()
            article['link'] = td.xpath("./a/@href").get()
            article['push_date'] = td.xpath(".//div[@class='caption']/span[last()]/text()").get()
            article['title'] = td.xpath(".//div[@class='tout__details']/h3/text()").get()
            article['text'] = td.xpath(".//div[@class='tout__details']/p/text()").get()
            yield article

    def parse_whitepapers(self, response):
        tds = response.xpath("//div[@class='columns']/div/div/article")
        for td in tds:
            article = NormalbankItem()
            article['link'] = BASE_URL + td.xpath("./a/@href").get()
            article['push_date'] = td.xpath(".//div[@class='caption']/span[last()]/text()").get()
            article['title'] = td.xpath(".//div[@class='tout__details']/h3/text()").get()
            article['text'] = td.xpath(".//div[@class='tout__details']/p/text()").get()
            yield article


    def parse(self, response):
        pass

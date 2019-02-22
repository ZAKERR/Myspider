# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem

HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer':'https://www.mckinsey.com/mgi/our-research/discussion-papers-and-briefings',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

BASE_URL = "https://www.mckinsey.com/"

class MckinseySpider(scrapy.Spider):
    name = 'mckinsey'
    allowed_domains = ['mckinsey.com']

    def start_requests(self):
        next_url = 'https://www.mckinsey.com/mgi/our-research/discussion-papers-and-briefings'
        yield scrapy.Request(url =next_url,headers=HEADERS,callback=self.parse_discussion)
        next_url = 'https://www.mckinsey.com/mgi/our-research'
        yield scrapy.Request(url=next_url,headers=HEADERS,callback=self.parse_research)
        next_url = 'https://www.mckinsey.com/featured-insights/artificial-intelligence'
        yield scrapy.Request(url=next_url,headers=HEADERS,callback=self.parse_artificial_intelligence)
        next_url = 'https://www.mckinsey.com/industries/financial-services/our-insights'
        yield scrapy.Request(url = next_url,headers=HEADERS,callback=self.parse_artificial_intelligence)
        next_url = 'https://www.mckinsey.com/business-functions/risk/our-insights'
        yield scrapy.Request(url =next_url,headers = HEADERS,callback=self.parse_artificial_intelligence)

    def parse_discussion(self,response):
        tds = response.xpath("//div[@id='main_0_universal_2_divBlockList']/div")
        for td in tds:
            article = NormalbankItem()
            article['link'] = BASE_URL + td.xpath(".//a/@href").get()
            article['push_date'] = td.xpath(".//time/text()").get()
            article['title'] = td.xpath(".//a/h3/text()").get()
            article['text'] = td.xpath(".//div[@class='description']/text()").get()
            yield article

    def parse_research(self,response):
        tds = response.xpath(".//div[@class='outer']/div/section")
        for td in tds:
            article = NormalbankItem()
            article['link'] = BASE_URL + td.xpath(".//a/@href").get()
            article['push_date'] = 'tag-end'
            article['text'] = 'tag-end'
            article['title'] = td.xpath('.//h3/text()').get()
            yield article


    def parse_artificial_intelligence(self,response):
        tds = response.xpath(".//div[@class='outer']/div[last()]/section")
        for td in tds:
            article = NormalbankItem()
            article['link'] = BASE_URL + td.xpath(".//a/@href").get()
            article['push_date'] = 'tag-end'
            article['text'] = 'tag-end'
            article['title'] = td.xpath('.//h3/text()').get()
            yield article

    def parse(self, response):
        pass

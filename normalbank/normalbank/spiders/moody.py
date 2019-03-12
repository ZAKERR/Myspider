# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem
import re
import json
BASE_URL = 'https://www.moodys.com'

LOGIN_DATA = {
    'UserName':'815608963@qq.com',
    'Password':'ROOT123123',
    'IsRememberMe':'false',
}

HEADERS = {
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin':'https://www.moodys.com',
    'Referer':'https://www.moodys.com/pages/default_ch.aspx',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

HEADERS_JSON1 = {
    "Accept":"application/json, text/plain, */*",
    "Host":"www.moodys.com",
    "Content-Type":"application/json",
    'Origin':'https://www.moodys.com',
    'Referer':'https://www.moodys.com/newsandevents/topics/Chinas-trade-off-Deleveraging-and-stability-00702A/research',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

HEADERS_JSON2 = {
    "Accept": "application/json, text/plain, */*",
    "Host": "www.moodys.com",
    "Content-Type": "application/json",
    'Origin': 'https://www.moodys.com',
    'Referer': 'https://www.moodys.com/newsandevents/topics/2019-Outlooks-00704A/research',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}


HEADERS_JSON3 = {
    "Accept": "application/json, text/plain, */*",
    "Host": "www.moodys.com",
    "Content-Type": "application/json",
    'Origin': 'https://www.moodys.com',
    'Referer': 'https://www.moodys.com/newsandevents/topics/Bank-Regulation-and-Capital-007012/research',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

HEADERS_JSON4 = {
    "Accept": "application/json, text/plain, */*",
    "Host": "www.moodys.com",
    "Content-Type": "application/json",
    'Origin': 'https://www.moodys.com',
    'Referer': 'https://www.moodys.com/newsandevents/topics/Financial-Stability-Risks-Asset-Bubbles-and-Corporate-Leverage-00702F/research?region=Asia_reg',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

HEADERS_JSON5 = {
    "Accept": "application/json, text/plain, */*",
    "Host": "www.moodys.com",
    "Content-Type": "application/json",
    'Origin': 'https://www.moodys.com',
    'Referer': 'https://www.moodys.com/newsandevents/topics/Growth-Macroeconomic-outlook-and-insights-on-fiscal-and-monetary-policies-007014/research?region=Asia_reg',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

HEADERS_JSON6 = {
    "Accept": "application/json, text/plain, */*",
    "Host": "www.moodys.com",
    "Content-Type": "application/json",
    'Origin': 'https://www.moodys.com',
    'Referer': 'https://www.moodys.com/newsandevents/topics/Rising-Trade-Tensions-007046/research?region=Asia_reg',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

HEADERS_JSON7 = {
    "Accept": "application/json, text/plain, */*",
    "Host": "www.moodys.com",
    "Content-Type": "application/json",
    'Origin': 'https://www.moodys.com',
    'Referer': 'https://www.moodys.com/newsandevents/topics/Technology-and-innovation-007044/research',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

DATA_1 = {"data":["00702A",{},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}
DATA_2 = {"data":["00704A",{},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}
DATA_3 = {"data":["007012",{},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}
DATA_4 = {"data":["00702F",{},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}
DATA_5 = {"data":["007014",{},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}
DATA_6 = {"data":["007046",{"region":["Asia_reg"]},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}
DATA_7 = {"data":["007044",{},{"pageSize":10,"pageIndex":0,"sortBy":"publication_dt","sortDir":"desc"}]}

class MoodySpider(scrapy.Spider):
    name = 'moody'
    allowed_domains = ['moodys.com']
    def start_requests(self):

        #将获取的cookie自动存入
        next_url = 'https://www.moodys.com/identity/login'
        yield scrapy.FormRequest(url =next_url,formdata=LOGIN_DATA,headers=HEADERS)

        # next_url = 'https://www.moodys.com/pages/default_ch.aspx'
        # yield scrapy.Request(url = next_url,headers=HEADERS,callback=self.parse_index)
        #
        # next_url = 'https://www.moodys.com/search?keyword=Series:%20Credit%20Outlook'
        # yield scrapy.Request(url=next_url,headers=HEADERS,callback=self.parse_credit_outlook)

        next_url = 'https://www.moodys.com/services/mdc-topics?name=getResearchListByDimId'
        yield scrapy.Request(url = next_url,method = 'post',body = json.dumps(DATA_1),headers=HEADERS_JSON1,callback=self.parse_main)
        yield scrapy.Request(url=next_url,method='post',body= json.dumps(DATA_2),headers=HEADERS_JSON2,callback=self.parse_main)
        yield scrapy.Request(url=next_url,method = 'post',body = json.dumps(DATA_3),headers=HEADERS_JSON3,callback=self.parse_main)
        yield scrapy.Request(url = next_url,method = 'post',body = json.dumps(DATA_4),headers=HEADERS_JSON4,callback=self.parse_main)
        yield scrapy.Request(url = next_url,method = 'post',body = json.dumps(DATA_5),headers=HEADERS_JSON5,callback=self.parse_main)
        yield scrapy.Request(url =next_url,method = 'post',body = json.dumps(DATA_6),headers=HEADERS_JSON6,callback=self.parse_main)
        yield scrapy.Request(url = next_url,method = 'post',body = json.dumps(DATA_7),headers=HEADERS_JSON7,callback=self.parse_main)

    def parse_index(self,response):
        tds = response.xpath("//div[@id='mdcTS2']/p")
        print(tds)
        print(len(tds))
        for td in tds:
            article = NormalbankItem()
            if td.xpath("./a/@href").get() == None: continue
            article['push_date'] = td.xpath("./font/font/text()").get()
            article['link'] = BASE_URL + td.xpath("./a/@href").get()
            article['title'] = td.xpath("./a/font/font/text()").get()
            article['text'] = 'tag-end'
            yield  article

    def parse_credit_outlook(self,response):
        tds = response.xpath(".//div[@class='result-details']/div")
        for td in tds:
            article = NormalbankItem()
            article['link'] = BASE_URL + td.xpath('.//a/@href').get()
            article['title'] = td.xpath(".//a/@data-analytics-link").get()
            article['push_date'] = td.xpath(".//a/@data-analytics-link").get()
            article['text'] = 'tag-end'
            yield article

    def parse_main(self,response):
        items = json.loads(response.text)['data']['researches']
        for item in items:
            if item['authorizationType'] == 'Unauthorized': continue
            article = NormalbankItem()
            article['title'] = item['title']
            article['link'] = BASE_URL + item['url']
            article['text'] = item['synopsis']
            article['push_date'] = item['publishDate']
            yield article



    def parse(self, response):
        pass

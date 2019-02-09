# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem
import json
import time
HEADERS_JSON = {
    "Content-Type":"application/json",
    "Referer":"https://www.fitchratings.com/site/search?content=headlines",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

HEADERS_NOR = {
    "Referer": "https://www.fitchratings.com/site/search?content=headlines",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

class FitchSpider(scrapy.Spider):
    name = 'fitch'
    allowed_domains = ['fitchsolutions.com']

    def start_requests(self):               #首网页站点，并传递下一个网页站点
        now_time = str(int(time.time()*100))
        URL = "https://www.fitchratings.com/api/v2/headlines?limit=20&offset=0&_={}"

        yield scrapy.Request(url =URL.format(now_time),callback=self.fitch_headlines,headers=HEADERS_JSON)

    def fitch_headlines(self, response):
        json_articles = json.loads(response.text)['items']
        for json_article in json_articles:
            article = NormalbankItem()
            article['title'] = json_article['title']
            article['push_date'] = json_article['date']
            article['link'] = "https://www.fitchratings.com" + json_article['link']
            article['text'] = json_article['text']
            yield article
        yield scrapy.Request(url = "https://www.fitchsolutions.com/white-papers",callback=self.fitch_white_papers,headers = HEADERS_NOR)

    def fitch_white_papers(self,response):   #第二个网页站点，继续传递给下一个站点
        tds = response.xpath("//div[@class='content']/article")
        for td in tds:
            article = NormalbankItem()
            article['title'] = td.xpath("./h2//text()").get().strip()
            article['link'] = "https://www.fitchratings.com" + td.xpath("./a/@href").get().strip()
            date = td.xpath("./p/text()[last()]").getall()
            date = "".join(date).strip()
            article['push_date'] = date
            article['text'] = td.xpath("./p/a/text()").get().strip()
            yield article

    def parse(self, response):
        pass


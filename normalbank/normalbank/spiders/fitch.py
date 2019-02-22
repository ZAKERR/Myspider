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
    fir = 0
    def start_requests(self):               #首网页站点，并传递下一个网页站点
        now_time = str(int(time.time()*100))
        URL = "https://www.fitchratings.com/api/v2/headlines?limit=20&offset=0&_={}"

        yield scrapy.Request(url =URL.format(now_time),callback=self.fitch_headlines,headers=HEADERS_JSON)
        # yield scrapy.Request(url ="https://www.fitchsolutions.com/structured-finance",callback=self.fitch_structured_finance,headers=HEADERS_NOR)

    def fitch_headlines(self, response):
        json_articles = json.loads(response.text)['items']
        for json_article in json_articles:
            article = NormalbankItem()
            article['title'] = json_article['title']
            article['push_date'] = json_article['date']
            article['link'] = "https://www.fitchratings.com" + json_article['link']
            article['text'] = json_article['text']
            yield article
        self.fir += 1
        yield scrapy.Request(url = "https://www.fitchsolutions.com/white-papers",callback=self.fitch_white_papers,headers = HEADERS_NOR)

    def fitch_white_papers(self,response):   #第二个网页站点，继续传递给下一个站点
        tds = response.xpath("//div[@class='content']/article")
        for td in tds:
            article = NormalbankItem()
            article['title'] = td.xpath("./h2//text()").get().strip()
            article['link'] = "https://www.fitchsolutions.com" + td.xpath("./a/@href").get().strip()
            date = td.xpath("./p/text()[last()]").getall()
            date = "".join(date).strip()
            article['push_date'] = date
            article['text'] = td.xpath("./p/a/text()").get().strip()
            yield article

        yield  scrapy.Request(url = "https://www.fitchsolutions.com/structured-finance",
                              callback=self.fitch_normal,headers=HEADERS_NOR)

        yield scrapy.Request(url="https://www.fitchsolutions.com/infrastructure-project-finance",
                             callback=self.fitch_normal, headers=HEADERS_NOR)

        yield scrapy.Request(url="https://www.fitchsolutions.com/country-risk-sovereigns",
                             callback=self.fitch_normal, headers=HEADERS_NOR)

        yield scrapy.Request(url="https://www.fitchsolutions.com/financial-institutions",
                             callback=self.fitch_normal, headers=HEADERS_NOR)

        yield scrapy.Request(url="https://www.fitchsolutions.com/corporates",
                             callback=self.fitch_normal, headers=HEADERS_NOR)

    def fitch_normal(self,response):
        tds = response.xpath("//main//article/div/article")
        for td in tds:
            article = NormalbankItem()
            article['title'] = td.xpath("./h2/a/text()").get()
            article['link'] = "https://www.fitchsolutions.com" + td.xpath("./h2/a/@href").get()
            article['push_date'] = td.xpath("./p/text()[last()]").get()
            article['text'] = td.xpath("./div/p/text()").get()
            yield article



    # def fitch_infrastructure_project_finance(self,response):
    #     tds = response.xpath("//main//article/div/article")
    #     for td in tds:
    #         article = NormalbankItem()
    #         article['title'] = td.xpath("./h2/a/text()").get()
    #         article['link'] = "https://www.fitchsolutions.com" + td.xpath("./h2/a/@href").get()
    #         article['push_date'] = td.xpath("./p/text()[last()]").get()
    #         article['text'] = td.xpath("./div/p/text()").get()
    #         yield article
    #     yield scrapy.Request(url="https://www.fitchsolutions.com/infrastructure-project-finance",callback=self.fitch_infrastructure_project_finance,headers=HEADERS_NOR

    def parse(self, response):
        pass


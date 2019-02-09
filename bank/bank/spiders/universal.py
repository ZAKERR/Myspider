# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from finalTech.utils import get_config
# from finalTech.rules import rules
# from finalTech import urls
# from finalTech.items import *

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bank.items import *
from bank.utils import get_config
from bank import urls
import json
import time
from bank.TechLoader import *

class UniversalSpider(CrawlSpider):
    name = 'universal'  #默认值
    def __init__(self,name,*args,**kwargs):
        config = get_config(name)
        self.config = config
        self.tag = "normal"
        start_urls = config.get('start_urls')

        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls =start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                self.start_urls = list(eval('urls.'+start_urls.get('method'))(*start_urls.get('args',[])))
            elif start_urls.get('type') == 'json':
                self.start_urls = list(eval('urls.'+start_urls.get('method'))())
                self.tag = "json"
        self.allowed_domains = config.get('allowed_domains')
        super(UniversalSpider, self).__init__(*args, **kwargs)

    # def parse_item(self, response):
    #     item = self.config.get('item')
    #     if item:
    #         cls = eval(item.get('class'))()
    #         loader = eval(item.get('loader'))(cls,response=response)
    #         for key,value in item.get('attrs').items():
    #             for extractor in value:
    #                 if extractor.get('method') == 'xpath':
    #                     loader.add_xpath(key,*extractor.get('args'),**{'re':extractor.get('re')})
    #                 if extractor.get('method') == 'xpath':
    #                     loader.add_css(key,*extractor.get('args'),**{'re':extractor.get('re')})
    #                 if extractor.get('method') == 'value':
    #                     loader.add_value(key,*extractor.get('args'),**{'re':extractor.get('re')})
    #                 if extractor.get('method') == 'attr':
    #                     loader.add_value(key,getattr(response,*extractor.get('args')))
    #             yield loader.load_item()

    # def parse_start_url(self,response):
    #     item = self.config.get('item')
    #     json_articles = json.loads(response.text)['items']
    #     BASE_URL = "https://www.fitchratings.com/"
    #     for json_article in json_articles:
    #         article = {}
    #         article['title'] = json_article['title']
    #         article['date'] = json_article['date']
    #         article['link'] = BASE_URL + json_article['link']
    #         article['text'] = json_article['text']
    #         cls = eval(item.get('class'))()
    #         loader = eval(item.get('loader'))(cls, response=response)
    #         loader.add_value('title',article['title'])
    #         loader.add_value('date',article['date'])
    #         loader.add_value('link',article['link'])
    #         loader.add_value('text',article['text'])
    #         yield  loader.load_item()


    def parse_start_url(self,response):
        item = self.config.get('item')
        end = 1
        if self.tag == "json":
            json_articles = json.loads(response.text)['items']
            end =  len(json_articles)
        else:
            end = len(response.xpath("//div[@class='content']/article"))
        if item:
            for x in range(end):                #json文件遍历每个字典元素
                cls = eval(item.get('class'))()
                loader = eval(item.get('loader'))(cls,response=response)
                for key,value in item.get('attrs').items():
                    for extractor in value:
                        if extractor.get('method') == 'xpath':
                            loader.add_xpath(key,extractor.get('args')[0].format(x+1),**{'re':extractor.get('re')})
                        if extractor.get('method') == 'css':
                            loader.add_css(key,extractor.get('args')[0].format(x+1),**{'re':extractor.get('re')})
                        if extractor.get('method') == 'value':
                            loader.add_value(key,extractor.get('args')[0].format(x+1),**{'re':extractor.get('re')})
                        if extractor.get('method') == 'attr':
                            loader.add_value(key,getattr(response,*extractor.get('args')))
                        if extractor.get('method') == 'direct':
                            loader.add_value(key,json_articles[x][extractor.get('name')])
                        if extractor.get('method') == 'extra':
                            loader.add_value(key,extractor.get('args')+json_articles[x][extractor.get('name')])
                yield loader.load_item()
    # def parse_item(self, response):
    #     print(33333333333)
    #     item = self.config.get('item')
    #     if item:
    #         cls = eval(item.get('class'))()
    #         loader = eval(item.get('loader'))(cls, response=response)
    #         # 动态获取属性配置
    #         for key, value in item.get('attrs').items():
    #             for extractor in value:
    #                 if extractor.get('method') == 'xpath':
    #                     loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
    #                 if extractor.get('method') == 'css':
    #                     loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
    #                 if extractor.get('method') == 'value':
    #                     loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
    #                 if extractor.get('method') == 'attr':
    #                     loader.add_value(key, getattr(response, *extractor.get('args')))
    #         yield loader.load_item()



# -*- coding: utf-8 -*-
import scrapy
from normalbank.items import NormalbankItem
import json
import re
BASE_URL = 'https://www.spglobal.com'

HEADERS = {
    "Referer": "https://www.spglobal.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

HEADERS_JS = {
    'Content-Type':'*/*',
    'Referer':'https://www.spglobal.com/en/research-insights/index',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

class SpglobalSpider(scrapy.Spider):
    name = 'spglobal'
    allowed_domains = ['spglobal.com','sandpglobal-spglobal-live.cphostaccess.com']

    def start_requests(self):
        yield scrapy.Request(url="https://www.spglobal.com/en/research-insights/index",callback=self.spglobal_index,headers=HEADERS)
        next_url = 'https://sandpglobal-spglobal-live.cphostaccess.com/crownpeaksearchproxy.aspx?q=https%3A%2F%2Fsearchg2-restricted.crownpeak.net%2Fsandpglobal-spglobal-live%2Fselect%3Fq%3D*%253A*%2520OR%2520id%253A(891868%255E1000000000000%2520OR%2520886835%255E100000000000%2520OR%2520742266%255E10000000000%2520OR%2520668567%255E1000000000%2520OR%2520796316%255E100000000%2520OR%2520654467%255E10000000%2520OR%2520584394%255E1000000%2520OR%2520788320%255E100000%2520OR%2520601715%255E10000)%26echoParams%3Dexplicit%26fl%3Dtitle%2Ccustom_i_article_id%2Ccustom_dt_meta_publish_date%2Ccustom_s_local_url%2Ccustom_s_cshtml_path%2Ccustom_s_sub_type%2Ccustom_s_meta_type%2Cscore%2Ccustom_s_division%2Ccustom_ss_contenttype%2Ccustom_ss_location%2Ccustom_ss_region%2Ccustom_ss_theme%2Ccustom_ss_author_thumbnails%2Ccustom_ss_authors%2Ccustom_ss_author_titles%2Ccustom_s_meta_videoid%26defType%3Dedismax%26wt%3Djson%26start%3D0%26rows%3D12%26fq%3Dcustom_s_type%3A(%22article%22%2C%20%22event%22)%26fq%3Dcustom_s_sub_type%3A(%22blog%22%2C%20%22news%22%2C%20%22research%22%2C%20%22event%22%2C%20%22podcast%22%2C%20%22video%22%2C%20%22article%22)%26fq%3Dcustom_s_division%3A(%22Market%20Intelligence%22%2C%20%22Platts%22%2C%20%22Corporate%22)%26facet%3Dtrue%26facet.mincount%3D1%26facet.field%3Dcustom_ss_theme%26facet.field%3Dcustom_ss_theme%26facet.limit%3D15%26sort%3Dscore%20desc%2C%20custom_dt_meta_publish_date%20desc%26f.custom_ss_theme.facet.sort%3Dindex%26f.custom_ss_theme.facet.sort%3Dindex%26json.wrf%3Dsearchg2_885062140305962'
        yield scrapy.Request(url=next_url, callback=self.spglobal_index2, headers=HEADERS_JS)
        next_url = 'https://sandpglobal-spglobal-live.cphostaccess.com/crownpeaksearchproxy.aspx?q=https%3A%2F%2Fsearchg2-restricted.crownpeak.net%2Fsandpglobal-spglobal-live%2Fselect%3Fq%3D*%253A*%26echoParams%3Dexplicit%26fl%3Dtitle%2Ccustom_i_article_id%2Ccustom_dt_meta_publish_date%2Ccustom_s_local_url%2Ccustom_s_cshtml_path%2Ccustom_s_meta_type%2Cscore%2Ccustom_s_division%2Ccustom_s_type%2Ccustom_s_sub_type%26defType%3Dedismax%26wt%3Djson%26start%3D0%26rows%3D10%26fq%3Dcustom_s_type%3Aarticle%26fq%3Dcustom_s_sub_type%3Anews%26fq%3Dcustom_s_division%3A%22Market%20Intelligence%22%26fq%3Dcustom_b_is_global_markets%3Afalse%26facet%3Dtrue%26facet.mincount%3D1%26facet.field%3Dcustom_ss_theme%26facet.limit%3D15%26sort%3Dcustom_dt_meta_publish_date%20desc%26f.custom_ss_theme.facet.sort%3Dindex%26json.wrf%3Dsearchg2_1467457817091904'
        yield scrapy.Request(url=next_url, callback=self.spglobal_index2, headers=HEADERS_JS)
        next_url = "https://sandpglobal-spglobal-live.cphostaccess.com/crownpeaksearchproxy.aspx?q=https%3A%2F%2Fsearchg2-restricted.crownpeak.net%2Fsandpglobal-spglobal-live%2Fselect%3Fq%3D*%253A*%26echoParams%3Dexplicit%26fl%3Dtitle%2Ccustom_s_title%2Ccustom_i_item_id%2Ccustom_s_local_url%2Ccustom_s_cshtml_path%2Ccustom_s_meta_type%2Ccustom_s_division%2Ccustom_ss_segment%2Ccustom_s_type%2Ccustom_s_sub_type%2Ccustom_ss_authors%2Ccustom_ss_author_titles%2Ccustom_ss_author_thumbnails%2Ccustom_ss_tags%2Ccustom_ss_location%2Ccustom_ss_region%2Ccustom_ss_producttype%2Ccustom_ss_contenttype%2Ccontent%2Ccustom_ss_freeform%2Ccustom_dt_meta_publish_date%26defType%3Dedismax%26wt%3Djson%26start%3D0%26rows%3D10%26fq%3Dcustom_s_type%3Aarticle%26fq%3Dcustom_s_sub_type%3Aresearch%26fq%3Dcustom_s_division%3A%22Market%20Intelligence%22%26facet%3Dtrue%26facet.mincount%3D1%26facet.field%3Dcustom_ss_segment%26facet.field%3Dcustom_ss_segment%26facet.field%3Dcustom_ss_contenttype%26facet.limit%3D20%26sort%3Dcustom_dt_meta_publish_date%20desc%26facet.range%3Dcustom_dt_meta_publish_date%26f.custom_dt_meta_publish_date.facet.range.start%3DNOW%2FYEAR-1YEAR%26f.custom_dt_meta_publish_date.facet.range.end%3DNOW%26f.custom_dt_meta_publish_date.facet.range.gap%3D%252B1MONTH%26f.custom_ss_segment.facet.sort%3Dindex%26f.custom_ss_segment.facet.sort%3Dindex%26f.custom_ss_contenttype.facet.sort%3Dindex%26json.wrf%3Dsearchg2_6597651232213013"
        yield scrapy.Request(url=next_url, callback=self.spglobal_index2, headers=HEADERS_JS)


    def spglobal_index(self,response):
        tds = response.xpath("//div[contains(@class,'carousel__wrapper')]/ul/li")
        for td in tds:
            article = NormalbankItem()
            article['title']  = td.xpath(".//h1/text()").get()
            article['link']  = BASE_URL + td.xpath("./a/@href").get()
            article['push_date'] = td.xpath(".//ul[@class ='meta-data']/li[last()]/text()").get()
            article['text'] = "tag-end"
            yield article


    def spglobal_index2(self,response):
        text = re.search("searchg2_\d+\((.+)\)$",response.text)
        tds = json.loads(text.group(1))['response']['docs']
        for td in tds:
            article = NormalbankItem()
            article['title'] = td['title']
            article['push_date'] = td['custom_dt_meta_publish_date']
            article['link'] = BASE_URL + td['custom_s_local_url']
            article['text'] = "tag-end"
            yield article


    def parse(self, response):
        pass

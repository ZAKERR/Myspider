# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class NormalbankPipeline(object):
    def process_item(self, item, spider):
        yield item


class Mysqlpipeline():
    def __init__(self,host,database,user,password,port,table):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.table = table


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            database = crawler.settings.get('MYSQL_DATABASE'),
            user = crawler.settings.get('MYSQL_USER'),
            password= crawler.settings.get('MYSQL_PASSWORD'),
            port = crawler.settings.get('MYSQL_PORT'),
            table = crawler.settings.get('MYSQL_TABLE')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()


    def process_item(self,item,spider):
        data = dict(item)
        #查询数据库是否有此文章
        sql = "SELECT * FROM article where title = %s"
        self.cursor.execute(sql,(data['title']))
        results = self.cursor.fetchall()
        if len(results) == 0:
            #为scrapy_time字段
            with open(r'D:\PYTHON_PRACTISE\综合练习\爬虫练习\Scrapy\normalbank\scrapy_time.txt','r',encoding='utf-8') as fn:
                times = fn.read()
            data['scrapy_time'] = times
            keys = ','.join(data.keys())
            values = ','.join(['%s'] * len(data))
            sql = 'insert into %s (%s) values (%s)' %(self.table,keys,values)
            self.cursor.execute(sql,tuple(data.values()))
            self.db.commit()
        return item






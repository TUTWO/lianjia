# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Item
import pymongo

class LianjiaPipeline(object):

    def form_crawler(self, crawler):
        # MongoDB数据库连接
        self.DB_URL = crawler.settings.get('MONGO_DB_URL', 'mongodb://localhost:27017')
        # 创建数据库
        self.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'lianjia')
        return self

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['lianjia']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db['ershoufang']
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item

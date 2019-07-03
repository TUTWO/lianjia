# -*- coding: utf-8 -*-
import os
import sys

import scrapy
from scrapy.cmdline import execute
from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Rule
from lianjia.items import LianjiaItem
from scrapy_redis.spiders import RedisCrawlSpider

import re

# class ErshoufangSpider(CrawlSpider):
class ErshoufangSpider(RedisCrawlSpider):
    name = 'ershoufang'
    # start_urls = ['http://cd.lianjia.com/ershoufang/']
    allowed_domains = ['cd.lianjia.com']
    redis_key = 'ershoufangspider:start_urls'



    # 成都房源每一页链接
    page_urls = LinkExtractor(allow=(r"cd.lianjia.com/ershoufang/.{,9}/"), deny=(r"ershoufang/r", r"ershoufang/.*[b-e]", r"ershoufang/.*[h-k]", r"ershoufang/.*[q-z]"))
    # 每套房源的详细页面链接
    house_detail = LinkExtractor(allow=(r"ershoufang/\d+.html"))

    rules = (
        Rule(page_urls, follow=True),
        Rule(house_detail, callback="parse_item", follow=False),
    )

    def parse_item(self, response):
        item = LianjiaItem()

        item['name'] = self.get_name(response)

        item['price'] = self.get_price(response)

        item['avg_price'] = self.get_avg_price(response)

        item['position'] = self.get_position(response)

        item['house_type'] = self.get_house_type(response)

        item['floor'] = self.get_floor(response)

        item['size'] = self.get_size(response)

        item['mortgage'] = self.get_mortgage(response)

        item['tags'] = self.get_tags(response)

        item['transportation'] = self.get_transpotation(response)

        item['img'] = self.get_img(response)

        yield item

    def get_name(self, response):
        name = response.xpath('/html/body/div[3]/div/div/div[1]/h1/text()').extract()
        if len(name):
            name = name[0]
        else:
            name = "NULL"
        return name

    def get_price(self, response):
        price = response.xpath('/html/body/div[5]/div[2]/div[2]/span//text()').extract()
        if len(price):
            price = " ".join('%s' % id for id in price)
        else:
            price = "NULL"
        return price

    def get_avg_price(self, response):
        avg_price = response.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span//text()').extract()
        if len(avg_price):
            avg_price = " ".join('%s' % id for id in avg_price)
        else:
            avg_price = "NULL"
        return avg_price

    def get_position(self, response):
        position = response.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]//text()').extract()
        if len(position):
            position = ",".join('%s' % id for id in position)
        else:
            position = "NULL"
        return position

    def get_house_type(self, response):
        house_type = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()').extract()
        if len(house_type):
            house_type = house_type[0]
        else:
            house_type = "NULL"
        return house_type

    def get_floor(self, response):
        floor = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()').extract()
        if len(floor):
            floor = floor[0]
        else:
            floor = "NULL"
        return floor

    def get_size(self, response):
        size = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()').extract()
        if len(size):
            size = size[0]
        else:
            size = "NULL"
        return size

    def get_mortgage(self, response):
        mortgage = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()').extract()
        if len(mortgage):
            mortgage = mortgage[0].replace(" ", "")
        else:
            mortgage = "NULL"
        return mortgage

    def get_tags(self, response):
        tags = response.xpath('/html/body/div[7]/div[1]/div[2]/div/div[1]/div[2]/a/text()').extract()
        if len(tags):
            tags = ",".join('%s' % id for id in tags).replace(' ', '')
        else:
            tags = "NULL"
        return tags

    def get_transpotation(self, response):
        transportation = response.xpath('/html/body/div[7]/div[1]/div[2]/div/div[4]/div[2]/text()').extract()
        if len(transportation):
            transportation = transportation[0].replace(' ', '')
        else:
            transportation = "NULL"
        return transportation

    def get_img(self, response):
        img = response.xpath('//*[@id="layout"]/div/div[2]/div[2]/img/@src').extract()
        if len(img):
            img = img[0]
        else:
            img = "NULL"
        return img
#
# if __name__ == '__main__':
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(["scrapy", "crawl", "ershoufang"])
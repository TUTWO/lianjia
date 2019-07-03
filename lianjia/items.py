# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LianjiaItem(Item):
    name = Field()
    price = Field()
    avg_price = Field()
    position = Field()
    house_type = Field()
    floor = Field()
    size = Field()
    mortgage = Field()
    tags = Field()
    transportation = Field()
    img = Field()
    pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZolprojectItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    model = scrapy.Field()
    phonePrice = scrapy.Field()
    pass


class ZolTitlelink(scrapy.Item):
    link = scrapy.Field()
    pass


class BookItems(scrapy.Item):
    bookName = scrapy.Field()
    original = scrapy.Field()
    anchor = scrapy.Field()
    introduction = scrapy.Field()
    bookImg = scrapy.Field()
    bookType = scrapy.Field()
    pass

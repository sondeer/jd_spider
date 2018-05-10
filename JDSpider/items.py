# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

    commit = scrapy.Field()

    shop = scrapy.Field()

    shop_href = scrapy.Field()

    #id
    ItemID = scrapy.Field()
    #原价
    ori_price = scrapy.Field()
    #现价
    cur_price = scrapy.Field()








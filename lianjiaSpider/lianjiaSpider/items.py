# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    house_url = scrapy.Field()
    house_price = scrapy.Field()
    title = scrapy.Field()
    house_location = scrapy.Field()
    house_zone = scrapy.Field()
    community= scrapy.Field()
    house_area = scrapy.Field()


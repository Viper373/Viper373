# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 讲师姓名
    title = scrapy.Field()  # 讲师职称
    desc = scrapy.Field()  # 讲师简介
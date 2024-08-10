# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Wangyi163Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 职位名称
    productName = scrapy.Field()  # 所属部门全称
    firstDepName = scrapy.Field()  # 所属部门简称
    workPlaceName = scrapy.Field()  # 工作城市
    postTypeFullName = scrapy.Field()  # 职位类别
    description = scrapy.Field()  # 岗位介绍
    requirement = scrapy.Field()  # 任职要求
    recruitNum = scrapy.Field()  # 招聘人数
    reqEducationName = scrapy.Field()  # 学历要求
    reqWorkYearsName = scrapy.Field()  # 工作经验要求
    updateTime = scrapy.Field()  # 发布日期
    # 下面2个变量主要是为了做通用的数据库表写入程序用的。
    table_fields = scrapy.Field()  # 字段名称
    table_name = scrapy.Field()  # 插入表的名称

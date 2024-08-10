import re

import scrapy
from itcast.items import MyspiderItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = ["https://www.itheima.com/teacher.html"]

    def parse(self, response):
        # with open("itcast.html", "wb") as f:
        #     f.write(response.body)
        # 获取所有的教师节点
        node_list = response.xpath("//div[@class='li_txt']")
        # print(len(node_list))
        # 遍历教师节点列表
        # print(node_list)
        for node in node_list:
            # temp = {}
            item = MyspiderItem()
            # xpath方法返回的是选择器对象列表，如果有多个值，使用extract()用于从选择器对象中提取数据（需要加上索引）；
            # 如果只有一个值，使用extract_first()则不需要加索引，并且不会报错（没有提取到数据则返回None）
            item["name"] = node.xpath("./h3/text()")[0].extract()
            item["title"] = node.xpath("./h4/text()")[0].extract()
            item["desc"] = re.sub("[\t\n\r]", "", node.xpath("./p/text()")[0].extract())
            yield item
        # print(response.url)
        # print(response.request.url)
        # print(response.headers)
        # print(response.request.headers)

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json


class MyspiderPipeline(object):
    def __init__(self):
        self.file = open('itcast.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 将item对象强转为字典，该操作只能在scrapy中使用
        item = dict(item)
        # 将字典数据序列化
        json_data = json.dumps(item, ensure_ascii=False) + ',\n'
        # 将数据写入文件
        self.file.write(json_data)
        # 默认使用完管道之后需要将数据返回给引擎
        return item

    def __del__(self):
        self.file.close()

import scrapy
import json
from datetime import datetime
from wangyi163.items import Wangyi163Item

next_page = 1  # 用来控制翻页的变量，主要是给URL传递参数


class JobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["163.com"]
    start_urls = ["https://hr.163.com/api/hr163/position/queryPage"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name = 'job'
        self.table_fields = ['name', 'productName', 'firstDepName', 'workPlaceName',
                             'postTypeFullName', 'description', 'requirement', 'recruitNum',
                             'reqEducationName', 'reqWorkYearsName', 'updateTime']
        # 模拟翻页

    def start_requests(self):
        url = self.start_urls[0]
        # 负载
        payload = {
            "currentPage": "1",
            "pageSize": "10"
        }
        yield scrapy.Request(
            url=url,
            body=json.dumps(payload),
            method='POST',
            callback=self.parse,
            headers={'Content-Type': 'application/json'}
        )

    def parse(self, response):
        temp = response.json()
        job_list = temp['data']['list']
        item = Wangyi163Item()
        item['table_fields'] = self.table_fields
        item['table_name'] = self.table_name
        for job in job_list:
            item['name'] = job['name']
            item['productName'] = job['productName']
            item['firstDepName'] = job['firstDepName']
            item['workPlaceName'] = str(job['workPlaceNameList']).replace('[', '').replace(']', '').replace("'", '')
            item['postTypeFullName'] = job['postTypeFullName']
            item['description'] = job['description'].replace('\t', '').replace('\n', '')
            item['requirement'] = job['requirement'].replace('\t', '').replace('\n', '')
            item['recruitNum'] = job['recruitNum']

            if job['reqEducationName'] is None or job['reqEducationName'] == '':
                item['reqEducationName'] = "学历不限"
            else:
                item['reqEducationName'] = job['reqEducationName']

            if job['reqWorkYearsName'] is None or job['reqWorkYearsName'] == '':
                item['reqWorkYearsName'] = "经验不限"
            else:
                item['reqWorkYearsName'] = job['reqWorkYearsName']

            item['updateTime'] = datetime.utcfromtimestamp(job['updateTime'] / 1000).strftime("%Y-%m-%d")
            # 处理数据
            yield item
        # 模拟翻页
        # 返回的数据中来判断是否为最后一页 true为最后一页
        page_stutas = temp['data']['lastPage']
        global next_page
        print(f"-----当前爬取到职位第{next_page}页-----")
        next_page += 1
        if not page_stutas:  # 回调出口
            payload = {
                "currentPage": f"{next_page}",
                "pageSize": "10"
            }
            url = self.start_urls[0]
            yield scrapy.Request(
                url=url,
                body=json.dumps(payload),
                method='POST',
                callback=self.parse,
                headers={'Content-Type': 'application/json'})

import re
import time
import urllib.request
from pprint import pprint

from DrissionPage.common import Keys
from DrissionPage.common import Actions
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup

import captcha


class Law:
    def __init__(self):
        self.ca = captcha.SlideCaptchaSolver()
        self.page = self.ca.page
        self.url = "https://credit.acla.org.cn/"

    def get_html(self):
        self.page.get(self.url)
        self.page.ele("tag:li@class=organ-list pull-left organ-lawfirm").click()
        self.page.ele('#keyWords').input("北京和儒律师事务所")
        self.page.ele('tag:a@class=blue-right pull-right').click()
        self.page.wait.ele_displayed(".search-result")
        self.page.run_js(r"js/browser.js")
        self.page.run_js(r"js/debugger.js")
        self.page.listen.start('https://static.homolo.net/credit/prototype/static/font/')
        """嵌入式滑块"""
        while True:
            self.ca.delete_img_folder()
            # 下载滑块和背景图，target.png 指的是滑块的图片。background.png指的是带有缺口的背景图
            try:
                self.page.ele('#slider-img').save(path="./img/", name='target.png')
                self.page.ele('#bg-img').save(path="./img/", name='background.png')
                x_distance = self.ca.get_distance_by_ddddocr()
                # 该网址缺口的计算得除2，因为下载的图片为600 × 300 px ，而在网页上的图片大小为300 × 150 px
                x_distance = x_distance / 2.23
                # 计算出的轨迹
                trajectory = self.ca.get_tracks(x_distance)
                # 进行移动
                self.ca.move_to_gap(slide_ele="#slider-move-btn", tracks=trajectory)
                time.sleep(0.2)
            except RuntimeError:
                self.page.refresh()
                self.page.wait.load_start()
                self.page.wait(3)
                self.page.run_js(r"js/browser.js")
                self.page.run_js(r"js/debugger.js")
            self.page.wait(3)
            success = self.page.ele('@text()=高级检索', timeout=0.5)
            if success:
                print("验证成功")
                break
            else:
                print("验证失败，正在重试...")
                time.sleep(1)
                continue
        self.page.wait.ele_displayed(".search-name-inner pull-left")
        self.page.ele('.search-name-inner pull-left').ele('tag:a').click()
        self.page.wait(2)
        font_url = self.page.listen.wait().url
        with urllib.request.urlopen(font_url) as response, open('./static/font.ttf', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        # uscc = self.page.ele('@text=统一社会信用代码：').next('tag:div').text  # 统一社会信用代码
        allow = self.page.s_ele('#allow').text  # 基本信息
        print(allow)
        # law = self.page.ele('#law').text  # 所内律师信息
        # check = self.page.ele('#check').text  # 年度检查考核信息
        # prize = self.page.ele('#prize').text  # 奖励信息
        # punish = self.page.ele('#punish').text  # 行政处罚信息
        # empPunish = self.page.ele('#empPunish').text  # 行业处分信息
        # branch = self.page.ele('#branch').text  # 分所信息
        # organ = self.page.ele('#organ').text  # 境外分支机构
        # pprint(uscc)


def main():
    law = Law()
    law.get_html()


if __name__ == '__main__':
    main()

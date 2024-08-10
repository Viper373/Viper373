# 获取viper3.top的所有文章内容
# 本代码针对于https://viper3.top/编写，不适用于其他博客
# 步骤：
# 1、获取页码链接
# 2、通过页码链接，获取所有文章链接
# 3、通过文章链接提取文章内容（难点）

import re
from typing import TextIO
import requests
from bs4 import BeautifulSoup
from urllib import parse


# 类名的明明应该采用大驼峰命名法，使用 CapWords 约定
class BlogContentInfo(object):
    def __init__(self, url: str):
        self.truncate = True
        self.pageURL = list()
        self.paperURL = list()
        self.url = url

    @staticmethod
    def getHTMLText(url: str) -> str:
        """
        此函数用于获取网页的html文档
        :param url: 博客页主页链接
        :return: 返回页面源代码
        """
        try:
            # 获取服务器的响应内容，并设置最大请求时间为6秒
            res = requests.get(url)
            # 判断返回状态码是否为200
            res.raise_for_status()
            # 设置该html文档可能的编码
            res.encoding = res.apparent_encoding
            # 返回网页HTML代码
            pageSource = res.text
            return pageSource
        except Exception as e:
            return f'产生异常:\n{e}'

    def getPageURL(self) -> list:
        """
        此函数用于获取页码链接
        :return: 返回页码链接列表
        """
        # 因为网页的设置，所以网站首页就为文章第一页 https://rfzf.top/ ，但也可以用 https://rfzf.top/page/1/ 访问
        self.pageURL.append(f"{self.url}page/1/")
        pageSource = self.getHTMLText(self.url)
        # 解析HTML代码
        soup = BeautifulSoup(pageSource, 'html.parser')
        # 模糊搜索HTML代码的所有包含href属性的<a>标签
        a_labels = soup.find_all('a', attrs={'href': True})
        # 获取所有<a>标签中的href对应的值，即超链接
        for a in a_labels:
            url = a.get('href')
            if re.search(f"{self.url}page/.*?", url) is not None:
                self.pageURL.append(url)
        self.pageURL = list(set(self.pageURL))
        return self.pageURL

    def getPaperURL(self) -> list:
        """
        此函数用于获取文章链接
        urlencode()	该方法实现了对 url 地址的编码操作
        unquote() 	该方法将编码后的 url 地址进行还原，被称为解码
        :return: 返回文章链接列表
        """
        for pageU in self.pageURL:
            demo = self.getHTMLText(pageU)
            soup = BeautifulSoup(demo, 'html.parser')
            a_labels = soup.find_all('a', attrs={'href': True})
            for a in a_labels:
                url = a.get('href')
                # 匹配是文章链接，语法 如果"https://viper3.top.*?/\d+/"不会空并且不是"https://viper3.top/page/\d+/"
                if re.search(f"{self.url}\d+/", url) is not None and re.search(f"{self.url}page/\d+/", url) is None:
                    url = parse.unquote(url)
                    self.paperURL.append(url)
        return list(set(self.paperURL))

    def getContent(self, url: str, writeToFile: bool = False) -> str:
        """
        此函数用于获取文章内容
        :param url: 文章链接
        :param writeToFile: 是否写入文件
        :return:
        """

        def write() -> TextIO:
            """
            此函数用于将文章内容写入Content.txt文件
            :return: 返回TextIO类型对象，方便将文件写入完成后关闭
            """
            file = open("Content.txt", mode='a+', encoding="UTF8")
            if self.truncate:
                # 清空文件内容
                file.truncate(0)
                self.truncate = False

            file.writelines(url + "\n")
            file.writelines(result + "\n")
            file.writelines("========================\n")
            return file

        resp = requests.get(url)
        pageSource = resp.text
        soup = BeautifulSoup(pageSource, 'html.parser')
        div = soup.select("#post_content")[0]
        # 删除标签
        result = re.sub(r'<.*?>', '', str(div))
        # 将错误编码的<和>重新编码
        result = result.replace("&lt;", "<").replace("&gt;", ">").replace("     ", "    \n")
        # 格式化内容
        result = "\n".join(line for line in result.splitlines() if line.strip() != "")
        result = result.replace(" ", "")
        if writeToFile:
            fileTextIO = write()
            fileTextIO.close()
        return result + "\n"

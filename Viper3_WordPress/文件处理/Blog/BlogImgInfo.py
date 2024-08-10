# 获取viper3.top的每篇文章中的图片
# 本代码针对于https://viper3.top/编写，不适用于其他博客
# 步骤：
# 1、获取页码链接
# 2、通过页码链接，获取所有文章链接
# 3、通过文章链接提取爬取图片（难点）
# 4、将图片保存到本地
import os
import requests
import re
from urllib import parse
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin  # 使用 pypinyin 库将中文转换为拼音

global img_url


# 类名的命名应该采用大驼峰命名法，使用CapWords约定

class BlogImgInfo(object):
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
            return f'发生异常:\n{e}'

    def getPageURL(self) -> list:
        """
        此函数用于获取页码链接
        :return: 返回页码链接列表
        """
        # 因为网页的设置，所以网站首页就为文章第一页 https://viper3.top/ ，但也可以用 https://viper3.top/page/1/ 访问
        self.pageURL.append(f"{self.url}page/1/")
        pageSource = self.getHTMLText(self.url)
        # 解析HTML代码
        soup = BeautifulSoup(pageSource, 'html.parser')
        # 模糊搜索HTML代码的所有包含href属性的<a>标签
        a_labels = soup.find_all('a', attrs={'href': True})
        # 获取所有<a>标签中的href对应的值，即页码链接
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

    def saveImagesToLocal(self, url: str, base_folder: str):
        try:
            # 获取文章页面的HTML内容
            article_source = self.getHTMLText(url)
            soup = BeautifulSoup(article_source, 'html.parser')

            # 查找所有带有 data-fancybox 属性值为 post-images 的 div 标签
            div_tags = soup.select('div[data-fancybox="post-images"]')

            # 如果没有找到 data-fancybox 属性为 post-images 的 div 标签，则使用 img 标签提取图片链接
            if not div_tags:
                div_tags = soup.find_all('img', attrs={'loading': 'lazy'})

            # 获取链接的最后几个数字作为目录名
            url_parts = url.split('/')
            folder_name = url_parts[-2]  # 倒数第2个部分是链接中的数字

            # 初始化图片计数器
            img_count = 0
            # 添加标记，表示图片下载开始
            print("-------图片下载开始-------")

            for tag in div_tags:
                if tag.name == 'div':
                    img_url = tag.get('href')
                elif tag.name == 'img':
                    img_url = tag.get('src')

                if img_url and img_url.startswith("http"):
                    # 检查图片链接前缀是否为 image.rfzf.top
                    if img_url.startswith("https://image.rfzf.top"):
                        # 将链接前缀替换为 image-rfzf-1304473591.cos.ap-beijing.myqcloud.com
                        img_url = img_url.replace("https://image.rfzf.top", "https://image-rfzf-1304473591.cos.ap-beijing.myqcloud.com")

                    try:
                        # 发送HTTP请求获取图片内容
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_data = img_response.content

                            # 获取图片文件名，将其解码为中文
                            img_name = os.path.basename(img_url)
                            img_name = parse.unquote(img_name)

                            # 构建完整的目录路径
                            folder_path = os.path.join(base_folder, folder_name)

                            # 如果目录不存在，则创建它
                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path, exist_ok=True)  # exist_ok=True 表示如果文件夹存在则不会报错

                            img_path = os.path.join(folder_path, img_name)

                            # 将图片数据写入本地文件
                            with open(img_path, 'wb') as img_file:
                                img_file.write(img_data)

                            # 增加图片计数器
                            img_count += 1

                        else:
                            # 打印下载失败的图片链接
                            print(f"下载失败: {img_url}")
                    except Exception as e:
                        # 打印保存图片时的错误信息
                        print(f"保存图片时出错 {img_url}: {e}")

            # 检查图片计数器，如果没有图片则输出信息
            if img_count == 0:
                print("-------该文章没有图片-------")
            # 添加标记，表示图片下载结束
            print("-------图片下载结束-------")
        except Exception as e:
            # 打印获取文章内容时的错误信息
            print(f"获取文章内容时出错 {url}: {e}")

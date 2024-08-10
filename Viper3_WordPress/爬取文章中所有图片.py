import requests
from bs4 import BeautifulSoup
import os
import time

global image_filename


def download_images(urls, folder_names):
    global image_filename
    for url, folder_name in zip(urls, folder_names):
        # 发送GET请求获取网页内容
        response = requests.get(url, proxies=None)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 创建文件夹来保存图片
        os.makedirs(folder_name, exist_ok=True)

        # 查找所有ID为primary的元素
        primary_elements = soup.find_all(id='primary')

        # 遍历所有ID为primary的元素
        for primary_element in primary_elements:
            # 在每个ID为primary的元素中查找所有图片
            image_elements = primary_element.find_all('img')

            # 获取图片元素数量
            num_images = len(image_elements)

            # 遍历所有图片元素
            for i in range(1, num_images - 1):
                # 获取图片URL
                image_url = image_elements[i]['src']

                # 判断图片链接是否为data URI、zanshang.png或ICO图标，如果是则跳过下载
                if image_url.startswith('data:') or image_url.endswith('zanshang.png') or image_url.endswith('.ico'):
                    continue

                try:
                    # 发送GET请求下载图片
                    image_response = requests.get(image_url)

                    # 提取图片文件名
                    image_filename = image_url.split('/')[-1]

                    # 保存图片到本地
                    with open(os.path.join(folder_name, image_filename), 'wb') as f:
                        f.write(image_response.content)

                    print(f"下载图片: {image_filename}")
                    time.sleep(0.5)  # 延迟0.5秒

                except requests.exceptions.RequestException as e:
                    print(f"图片下载失败: {image_filename}，请手动下载")

        print(f"{folder_name}文章图片已爬取完成")
        time.sleep(1)  # 延迟1秒

    print("所有文章图片已爬取完成")


# 输入文章链接列表和文件夹命名列表
article_urls = ['https://viper3.top/?p=1117', 'https://viper3.top/?p=1122', 'https://viper3.top/?p=952',
                'https://viper3.top/?p=944', 'https://viper3.top/?p=917', 'https://viper3.top/?p=907',
                'https://viper3.top/?p=885', 'https://viper3.top/?p=857', 'https://viper3.top/?p=828',
                'https://viper3.top/?p=805', 'https://viper3.top/?p=764', 'https://viper3.top/?p=637',
                'https://viper3.top/?p=492', 'https://viper3.top/?p=534', 'https://viper3.top/?p=313',
                'https://viper3.top/?p=134', 'https://viper3.top/?p=137', 'https://viper3.top/?p=107',
                'https://viper3.top/?p=943']
folder_names = ['1117', '1122', '952', '944', '917', '907', '885', '857', '828', '805', '791', '764', '637', '492',
                '534', '313', '134', '137', '107', '943']

# 调用函数下载图片
download_images(article_urls, folder_names)

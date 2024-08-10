# 导入数据请求模块 (需要安装 pip install requests)
import requests
# 导入正则表达式模块 (内置模块, 不需要安装)
import re
# 解码 (内置模块, 不需要安装)
from urllib.parse import unquote
# 导入json (内置模块, 不需要安装)
import json
# 导入格式化输出模块 (内置模块, 不需要安装)
from pprint import pprint
# 导入自动化模块 (需要安装 pip install DrissionPage)
from DrissionPage import ChromiumPage
import time
# 打开浏览器
driver = ChromiumPage()
# 监听数据包
driver.listen.start('/aweme/v1/web/aweme/post')
# 访问网站
driver.get('https://www.douyin.com/user/MS4wLjABAAAAkzRSrOuSsM4Z1Ricsddumx_aSvX0jmOPcQR2qTs3PEtImBD8BomLrqvtIOBKOL0P')
for page in range(10):
    driver.scroll.to_bottom()
    # 等到数据包加载
    resp = driver.listen.wait()
    # 直接获取数据包内容
    JsonData = resp.response.body
    # 提取视频信息所在列表
    v_list = JsonData['aweme_list']
    # for循环遍历
    for index2 in v_list:
        video_id = index2['aweme_id']
        """发送请求"""
        # 模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        # 请求网址
        url = f'https://www.douyin.com/user/MS4wLjABAAAAkzRSrOuSsM4Z1Ricsddumx_aSvX0jmOPcQR2qTs3PEtImBD8BomLrqvtIOBKOL0P?modal_id={video_id}'
        # 发送请求
        response = requests.get(url=url, headers=headers)
        # 获取响应数据
        html = response.text
        # 结构化输出html
        # 解析数据, 提取视频链接
        info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', html)[0]
        # 进行解码 json字符串
        res = unquote(info)
        # 把json字符串转成json字典
        json_data = json.loads(res)
        # 提取视频链接
        video_url = 'https:' + json_data['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][0]['src']
        # 提取标题
        old_title = json_data['app']['videoDetail']['desc']
        # 替换特殊字符
        title = re.sub(r'[\\/"*?<>|\n]', '', old_title)
        # 发送请求 获取视频数据
        video_content = requests.get(url=video_url, headers=headers).content
        # 保存数据
        with open('video\\' + title + '.mp4', mode='wb') as f:
            # 写入数据
            f.write(video_content)

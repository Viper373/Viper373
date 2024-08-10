"""
[课程内容]: Python 爬虫 之 抖音视频采集

[上课时间]: 20:05

[授课老师]: 青灯教育-巳月

[知识点]:
    动态数据抓包
    requests发送请求
    X-Bogus 参数逆向

[开发环境]:
    python 3.8               运行代码
    pycharm 2022.3           辅助敲代码
    requests                 pip install requests

[没听懂?]
课后的回放录播资料找落落老师微信
+python安装包 安装教程视频
+pycharm 社区版 专业版 及 激活码免费

零基础 0
有基础 1

什么是爬虫?
    作用: 批量 采集数据 以及 模拟用户行为
    原理: 模拟成 客户端 向 服务器 发送网络请求

分析数据来源
    找到作品链接

https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAqsOmrExIsJbZ2b0QLzytzAhAFbJUROH72_yVYM7Zq8E&max_cursor=0&locate_item_id=7273024102460362047&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=116.0.0.0&browser_online=true&engine_name=Blink&engine_version=116.0.0.0&os_name=Windows&os_version=10&cpu_core_num=6&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7206570248416773684&msToken=5tGWEtdYSWlzOgB96wdvpSwDH3wwbSwp5UFDBc8wBZk9LOMycvwvFaZ9HB4TP6vGrr4bW8I-DjKo3_Csn9SZSrD6llhIDlFoj3EEz7rRBcJLKZrRyDufL4XkeO0idCY=&X-Bogus=DFSzswVOvYiANSVTtyeXaVXAIQ5p

核心编程    2260
爬虫开发    2980
数据分析    2180
网站开发    2980
JS逆向课    1680

工作  7个月     8880 - 500 = 8380 / 18 = 465.55
    核心编程    2
    爬虫开发    2
    数据分析    1
    网站开发    2
    一线城市 80% 以上 8-15k 薪资区间
兼职  5个月     6680 - 300 = 6380 / 18 = 354.44
    核心编程    2
    爬虫开发    2
    数据分析    1

    学会如何 找外包
兴趣  4个月     4660 - 100 = 4560 / 12 = 380
    爬虫开发    2
    JS逆向课   2   1680
省时间

每周 135 / 246 晚上 8-10 直播和授课
课后 录播 + 老师一对一解答辅导
课后 作业
阶段 考核
"""
import requests
import execjs


ctx = execjs.compile(open('x_bogus.js', mode='r', encoding='utf-8').read())
headers = {
    'referer': 'https://www.douyin.com/user/MS4wLjABAAAAqsOmrExIsJbZ2b0QLzytzAhAFbJUROH72_yVYM7Zq8E?vid=7273024102460362047',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
arg1 = 'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAqsOmrExIsJbZ2b0QLzytzAhAFbJUROH72_yVYM7Zq8E&max_cursor=1690869936000&locate_item_id=7273024102460362047&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=dy_17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=116.0.0.0&browser_online=true&engine_name=Blink&engine_version=116.0.0.0&os_name=Windows&os_version=10&cpu_core_num=6&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7206570248416773684&msToken=kuJ7VXEum5t8MRJsb-EWiKneHuMabLt_Xmvzqjv7Tl92qzTPYaHkfIMCn9ndAkA39d7QfcI57AU353tQuNpAnxbsgxSEXN6KR4Du5bRKUrivq2hBvPiEPaFyW0xyaMc='
url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?'
xb = arg1 + '&X-Bogus=' + ctx.call('window.get_xb', arg1)
url += xb
print(url)
response = requests.get(url, headers=headers)
json_data = response.json()
aweme_list = json_data['aweme_list']
for aweme in aweme_list:
    desc = aweme['desc']
    video_url = aweme['video']['play_addr']['url_list'][0]
    print(desc, video_url)
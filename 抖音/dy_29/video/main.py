import random
import time
from pprint import pprint

import requests
from urllib.parse import urlencode
import execjs
import json
from pathlib import Path
from base_config.check_config import CheckConfig


class Video:

    def __init__(self):
        self.nickname = "未知昵称"
        self.user_age = "未知年龄"
        self.unique_id = "未知抖音号"
        self.follower_count = "未知粉丝量"
        self.country = "未知国家"
        self.province = "未知省份"
        self.city = "未知城市"
        self.school_name = "未知学校"
        self.ip = "未知IP"
        self.aweme_count = 0
        self.sec_user_id = None
        self.max_cursor = "0"
        self.has_more = "1"
        self.data_path = Path(f"{Path(__file__).parent}/{Path('data')}")
        self.data_path.mkdir(exist_ok=True)
        self.blogger_ids = []
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
            "referer": "https://www.douyin.com/user/MS4wLjABAAAAs0bM12zNkgYfwA-cPqxmitV_qBceJdi10wA8Qw044BU?vid=7342603062198013236",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        self.cookies = {
            "ttwid": "1%7CknRGIV--4WkEeXC_G6k0VRuRNJFWjVAsQkM-gKMjBtY%7C1709010665%7C0e18e44e5b4f77ef12f83a7d0cee1d866b503074b668ba4d9061930564e6b8ec",
        }
        self.ctx = execjs.compile(open('../js/a_bogus.js', 'r', encoding='utf-8').read())

        self.other_api = "https://www.douyin.com/aweme/v1/web/user/profile/other/"
        self.post_api = "https://www.douyin.com/aweme/v1/web/aweme/post/"

    @staticmethod
    def read_bloggers():
        """
        读取配置文件，返回所有sec_user_id的列表
        """
        check_config = CheckConfig()
        # 检查并可能重新生成配置文件
        check_config.check_and_generate_config()
        try:
            with open(check_config.filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
                blogger_ids = [blogger["sec_user_id"] for blogger in config.get("bloggers", [])]
                return blogger_ids
        except FileNotFoundError:
            # 如果即使在尝试生成后仍找不到文件，返回空值
            print(f"配置文件'{check_config.filename}'未找到")
            print(
                f"请运行{Path(__file__).parent}/'{next((d for d in Path(__file__).parent.iterdir() if d.is_dir() and 'config' in d.name), None)}'下{Path(__file__).parent.glob('generate*.py')}以重新生成配置文件")
            return "", []
        except json.JSONDecodeError:
            # 如果配置文件存在但不是有效的JSON，也返回空值
            print(f"配置文件'{check_config.filename}'格式错误，请检查")

    @staticmethod
    def read_storage():
        """
        读取配置文件，返回storage_folder路径
        """
        check_config = CheckConfig()
        # 检查并可能重新生成配置文件
        check_config.check_and_generate_config()
        try:
            with open(check_config.filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
                storage_folder = config.get("storage_folder", "")
                return storage_folder
        except FileNotFoundError:
            # 如果即使在尝试生成后仍找不到文件，返回空值
            print(f"配置文件'{check_config.filename}'未找到")
            print(
                f"请运行{Path(__file__).parent}/'{next((d for d in Path(__file__).parent.iterdir() if d.is_dir() and 'config' in d.name), None)}'下{Path(__file__).parent.glob('generate*.py')}以重新生成配置文件")
            return "", []
        except json.JSONDecodeError:
            # 如果配置文件存在但不是有效的JSON，也返回空值
            print(f"配置文件'{check_config.filename}'格式错误，请检查")

    def bloggers_video(self, blogger_ids, data_path):
        for blogger_id in blogger_ids:
            start_time = time.time()
            # noinspection PyDictCreation
            self.sec_user_id = blogger_id
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "sec_user_id": f"{self.sec_user_id}",
                "max_cursor": f"{self.max_cursor}",
                "locate_item_id": "7342603062198013236",
                "locate_query": "false",
                "show_live_replay_strategy": "1",
                "need_time_list": "1",
                "time_list_query": "0",
                "whale_cut_token": "",
                "cut_version": "1",
                "count": "18",
                "publish_video_strategy_type": "2",
                "pc_client_type": "1",
                "version_code": "290100",
                "version_name": "29.1.0",
                "cookie_enabled": "true",
                "screen_width": "1920",
                "screen_height": "1080",
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "123.0.0.0",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "123.0.0.0",
                "os_name": "Windows",
                "os_version": "10",
                "cpu_core_num": "8",
                "device_memory": "8",
                "platform": "PC",
                "downlink": "10",
                "effective_type": "4g",
                "round_trip_time": "50",
                "webid": "7284091090171938345",
                "msToken": "RDJcTjP-OTeaBVy5LypM_lPMQ2P_JbRtvDxSebSmlIEPRJRqDusmEKQ_9gZWQp5NaJZms7IicmGpb4x0QNz3Ledekoe20wAHfn228P2c"
            }
            a_bogus = self.ctx.call('getabs', {
                "params": urlencode(params),
                "body": "",
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            })
            params['a_bogus'] = a_bogus

            other_response = requests.get(url=self.other_api, headers=self.headers, cookies=self.cookies, params=params)
            u_dic = json.loads(other_response.text)['user']
            try:
                self.nickname = u_dic['nickname']  # 作者名称
            except:
                pass
            try:
                if u_dic['user_age'] == "" or u_dic['user_age'] is None:
                    pass
            except:
                self.user_age = f"{u_dic['user_age']}岁"  # 作者年龄
            try:
                self.unique_id = f"抖音号：{u_dic['unique_id']}"  # 作者抖音号
            except:
                self.unique_id = f"抖音号：{u_dic['short_id']}"  # 作者抖音号
            try:
                self.follower_count = f"粉丝：{round(u_dic['follower_count'] / 10000, 1)}万"  # 粉丝量
            except:
                pass
            try:
                if u_dic['country'] == "" or u_dic['country'] is None:
                    pass
            except:
                self.country = u_dic['country']  # IP-国家
            try:
                if u_dic['province'] == "" or u_dic['province'] is None:
                    pass
            except:
                self.province = u_dic['province']  # IP-省
            try:
                if u_dic['city'] == "" or u_dic['city'] is None:
                    pass
            except:
                self.city = u_dic['city']  # IP-市
            try:
                if u_dic['school_name'] == "" or u_dic['school_name'] is None:
                    pass
            except:
                self.school_name = u_dic['school_name']  # 学校

            self.ip = f'IP：{self.country}·{self.province}·{self.city}·{self.school_name}'  # IP-总
            try:
                self.aweme_count = f"作品数量：{u_dic['aweme_count']}"  # 作品数量
            except:
                pass

            filename = f"{self.nickname}_{self.user_age}_{self.unique_id}_{self.follower_count}_{self.ip}_{self.aweme_count}"  # 定义单个博主视频目录名称
            self.data_path = data_path
            user_dir = self.data_path / Path(filename)  # 准备创建单个博主视频目录
            user_dir.mkdir(exist_ok=True)  # 确保用户目录存在

            print(f"正在获取{self.nickname}的作品，共计作品数量：{u_dic['aweme_count']}")
            while self.has_more == "1":
                post_response = requests.get(url=self.post_api, headers=self.headers, cookies=self.cookies, params=params)
                v_JsonData = json.loads(post_response.text)

                v_list = v_JsonData['aweme_list']  # 提取视频信息所在列表
                for video in v_list:
                    desc = video['desc']
                    video_url = video['video']['play_addr']['url_list'][0]
                    video_content = requests.get(url=video_url).content

                    with open(f"{self.data_path}/{filename}/{desc}.mp4", mode='wb') as f:
                        # 写入数据
                        f.write(video_content)

                # 重新对params赋值
                self.max_cursor = str(v_JsonData['max_cursor'])
                self.has_more = str(v_JsonData['has_more'])
                a_bogus = self.ctx.call('getabs', {
                    "params": urlencode(params),
                    "body": "",
                    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                })
                params['max_cursor'] = self.max_cursor
                params['a_bogus'] = a_bogus
                params['need_time_list'] = "0"

                time.sleep(random.randint(1, 3))
            time.sleep(random.randint(2, 5))

            end_time = time.time()
            total_duration_seconds = int(end_time - start_time)
            minutes = total_duration_seconds // 60
            seconds = total_duration_seconds % 60
            print(f"{self.nickname}作品已下载完毕，共计耗时{minutes}分{seconds} 秒")

            # 移除max_cursor和has_more，防止参数错误，用于请求下一个博主other_api
            params.pop('max_cursor')
            params['need_time_list'] = "1"


def main():
    check_config = CheckConfig()
    check_config.check_and_generate_config()
    video = Video()
    print(f"数据默认存储至{Path(__file__).parent / video.data_path}，是否需要使用配置文件中的数据存储目录？")
    print("是（Y/y） 否（N/n）")
    while True:
        choice = input()
        if choice == 'Y' or choice == 'y':
            try:
                video.data_path = video.read_storage()
                video.blogger_ids = video.read_bloggers()
                print(f"配置文件'{check_config.filename}'存在且有效")
                print("正在获取博主作品...")
                break
            except:
                print(
                    f"配置文件'{check_config.filename}'不存在或无效，请检查{Path(__file__).parent}/'{next((d for d in Path(__file__).parent.iterdir() if d.is_dir() and 'config' in d.name), None)}'下{Path(__file__).parent.glob('*.json')}配置文件")
        elif choice == 'N' or choice == 'n':
            if video.read_bloggers():
                video.data_path = Path(__file__).parent / video.data_path
                print(f"配置文件'{check_config.filename}'存在且有效")
                print("正在获取博主作品...")
                break
        else:
            print("输入有误，请重新输入！")
    video.bloggers_video(video.blogger_ids, video.data_path)


if __name__ == '__main__':
    main()

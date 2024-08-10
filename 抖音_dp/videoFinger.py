from pathlib import Path
import random
import time
from pprint import pprint
import requests
import re
import json
import warnings
# 解码
from urllib.parse import unquote
# 导入验证码模块
import captcha
from DrissionPage import ChromiumPage, ChromiumOptions
warnings.filterwarnings("ignore")

global response


class Video:

    def __init__(self):
        co = ChromiumOptions()
        user_data_path = "C:\\Users\\24835\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2"
        co.set_user_data_path(user_data_path)
        # 设置启动时最大化
        co.set_argument('--start-maximized')
        self.driver = ChromiumPage(addr_or_opts=co)
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
        self.captcha_solver = captcha.SlideCaptchaSolver()
        self.phone_number = None
        self.password = None
        # 获取当前脚本文件的目录
        self.project_dir = Path(__file__).parent
        # 定位视频目录
        self.video_dir = self.project_dir / "video"
        # 确保视频目录存在
        self.video_dir.mkdir(exist_ok=True)
        # self.proxies = {
        #     "http": "http://t11169343635831:natjpxr6@m326.kdltps.com:15818/",
        #     "https": "http://t11169343635831:natjpxr6@m326.kdltps.com:15818/"
        # }

    "@Override"

    def solve_captcha1(self):
        """嵌入式滑块，使用无限重试机制。"""
        try:
            while True:
                # 假设 delete_img_folder 清理图片文件夹的方法存在
                self.captcha_solver.delete_img_folder()
                self.driver.ele('.web-login-trusted__other-login').ele('tag:span').click()  # 点击其他方式登录按钮
                self.driver.ele('text=密码登录').click()  # 点击密码登录按钮
                self.driver.ele('.web-login-normal-input__input').input(self.phone_number)  # 输入手机号
                self.driver.ele('.web-login-button-input__input').input(self.password)  # 输入密码
                self.driver.ele('@@type=submit@@class:web-login-button').click()  # 点击登录按钮
                if self.driver.ele('.btn-title', timeout=0.5):
                    print("无需验证码，登录成功")
                else:
                    self.driver.wait.load_start()  # 等待验证码出现
                    self.driver.ele('.vc-captcha-refresh--text').click()  # 点击验证码刷新按钮
                    # 下载滑块和背景图
                    self.driver.ele('.captcha-verify-image').save(path="./img/", name='target.png')
                    self.driver.ele('.captcha-verify_img_slide').save(path="./img/", name='background.png')

                    x_distance = self.captcha_solver.get_distance_by_ddddocr()  # 假设该方法返回正确的滑块距离
                    x_distance /= 2  # 根据实际图片大小调整

                    trajectory = self.captcha_solver.get_tracks(x_distance)  # 假设该方法基于距离生成拖动轨迹
                    self.captcha_solver.move_to_gap(slide_ele=".captcha-slider-btn", tracks=trajectory)
                    time.sleep(3)

                    # 检查验证是否成功
                    success = self.driver.ele('.btn-title', timeout=0.5)
                    if success:
                        print("验证码通过成功，登录成功")
                        break
                    else:
                        print("验证码通过失败，正在重试...")
                        time.sleep(1)
                    # 对验证码页面进行截图
                    captcha1 = self.driver.ele('#shumei_form_captcha_wrapper')
                    if captcha1:
                        captcha1.get_screenshot(path="./img/captcha1.png")
        except:
            pass

    def close_driver(self):
        self.driver.quit()

    def video_spider(self, blogger_urls):
        # 定义一个包含多个博主主页的列表

        # 遍历每个博主的URL
        global response
        for blogger_url in blogger_urls:
            captcha_solver = captcha.SlideCaptchaSolver()  # 初始化验证码模块
            # 监听用户信息数据包（要在get请求之前）
            self.driver.listen.start('/aweme/v1/web/user/profile/other')
            # 访问网站
            self.driver.get(blogger_url)
            self.driver.wait.ele_displayed('body')
            try:
                captcha.SlideCaptchaSolver.solve_captcha1(captcha_solver)
            except:
                pass
            time.sleep(random.randint(2, 3))
            # 当退出循环时，假设已经加载了所有内容
            profile_resp = self.driver.listen.wait()
            u_JsonData = profile_resp.response.body
            u_dic = u_JsonData['user']
            try:
                # 作者名称
                self.nickname = u_dic['nickname']
            except:
                pass
            # 作者年龄
            try:
                self.user_age = f"{u_dic['user_age']}岁"
            except:
                pass
            try:
                # 作者ID
                self.unique_id = f"抖音号：{u_dic['unique_id']}"
            except:
                pass
            try:
                # 粉丝量
                self.follower_count = f"粉丝：{round(u_dic['follower_count'] / 10000, 1)}万"
            except:
                pass
            try:
                # IP-国家
                self.country = u_dic['country']
            except:
                pass
            try:
                # IP-省
                self.province = u_dic['province']
            except:
                pass
            try:
                # IP-市
                self.city = u_dic['city']
            except:
                pass
            try:
                # 学校
                self.school_name = u_dic['school_name']
            except:
                pass
            # IP-总
            self.ip = f'IP：{self.country}·{self.province}·{self.city}·{self.school_name}'
            try:
                # 作品数量
                self.aweme_count = f"作品数量：{u_dic['aweme_count']}"
            except:
                pass
            filename = f"{self.nickname}_{self.user_age}_{self.unique_id}_{self.follower_count}_{self.ip}_{self.aweme_count}"
            user_dir = self.video_dir / filename
            # 确保用户目录存在
            user_dir.mkdir(exist_ok=True)
            # 监听用户作品数据包
            self.driver.listen.start('/aweme/v1/web/aweme/post')
            # 刷新页面，目的是获取作品数据包
            self.driver.refresh()
            time.sleep(random.randint(3, 4))
            while True:
                last_height = self.driver.run_js("return document.body.scrollHeight")
                while True:
                    # 滚动到页面底部
                    self.driver.run_js("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # 稍等片刻，等待页面加载
                    # 检查页面高度是否增加，如果没有增加，则停止滚动
                    new_height = self.driver.run_js("return document.body.scrollHeight")
                    if new_height == last_height:
                        break  # 如果高度没有变化，则假设已到达页面底部
                    last_height = new_height
                time.sleep(random.randint(2, 3))
                # 等到数据包加载
                video_resp = self.driver.listen.wait()
                # 直接获取数据包内容
                v_JsonData = video_resp.response.body
                # 提取视频信息所在列表
                v_list = v_JsonData['aweme_list']
                # for循环遍历
                for video in v_list:
                    video_id = video['aweme_id']
                    """发送请求"""
                    # 模拟浏览器
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.5.22 NetType/WIFI Language/zh_CN',
                    }
                    # 请求网址
                    url = f'{blogger_url}?modal_id={video_id}'
                    count = 0
                    while count <= 3:
                        # 发送请求
                        try:
                            response = requests.get(url=url, headers=headers)
                            # 获取响应数据
                            html = response.text
                            pprint(html)
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
                            with open(f"{self.video_dir}/{filename}/{title}.mp4", mode='wb') as f:
                                # 写入数据
                                f.write(video_content)
                            break
                        except Exception as e:
                            print(f"{response} {e} 重试第{count + 1}次")
                            count += 1
                            time.sleep(random.randint(7, 10))
                            continue


def main():
    blogger_urls = [
        "https://www.douyin.com/user/MS4wLjABAAAAkzRSrOuSsM4Z1Ricsddumx_aSvX0jmOPcQR2qTs3PEtImBD8BomLrqvtIOBKOL0P",  # 一口奶盖
        "https://www.douyin.com/user/MS4wLjABAAAA_5hZFZR2NS0gEEhF_f3SE65XgLm5FrQFan_iI2ZwY0g",  # 问枫
        "https://www.douyin.com/user/MS4wLjABAAAAKKjfYUn_-Pm6NX1tcFXdu3Eceqb3Z9xSpV3uwWMddZctHHjrJCc8_7FK4iFs1jPv",  # 布蕾BURY🐰
        "https://www.douyin.com/user/MS4wLjABAAAAVZCp6OaG9dKlEpRYL_4Dj5mxZkLegrQbaYFEYW00zrw",  # 赫宜
        "https://www.douyin.com/user/MS4wLjABAAAAI5iu6CLV9EQCzlZKCPf2I1aj1WRTYWAU2HZBBwq9GeQ",  # 冰淇淋の 酱
        "https://www.douyin.com/user/MS4wLjABAAAAgvWLSkGJiMkk7D854fyaGiMQSJ8GsUZf6BB4ma6GJS1zPzoz0qKQvC9xBQEs49p5",  # 2.0
        "https://www.douyin.com/user/MS4wLjABAAAAafzqFeXdiuc8nx_YYWlt5kkaaTyrtr1S7s8tW94pVrJ-ot2ibqU4qSKA_eNBTJLl",  # 小甜奈奈崽
        "https://www.douyin.com/user/MS4wLjABAAAAGdKTuWSzn_dnX7VrFdrj-59g34YRqbIAGulPBq3dEUooPWgbpeQykJ0lqXEUkyvr",  # 烟熏肉好好次
        "https://www.douyin.com/user/MS4wLjABAAAAwOvtgolWQ02B-4OFI0k7Avou36H7_2gKM6WyhL7ctCE",  # 小椿
        "https://www.douyin.com/user/MS4wLjABAAAAcgRrkCZ4sOA7fxBA9Z23AUqGJfp5pH_l8pSvFUCME6_hhplzKnT6H5umqRE2rhIK"  # 露娜鸭
        "https://www.douyin.com/user/MS4wLjABAAAAWrnPiIDDdz6zAE8p8Fi47EGhyu8LUzMk7dNpCs7CwSM",  # 小茜永远滴神
        "https://www.douyin.com/user/MS4wLjABAAAADlrkr8_SYSAiuXcHYZ2NUeyfdFWBhm9HeemwivNt71w_DrdNG9W9AyCIo1PbG_Jy",  # 小甜鱼
        "https://www.douyin.com/user/MS4wLjABAAAAPiSgzHO6xi_43V8yXT3_pr5RDLtOnIluYEzxuThkLrE7goNH-zAfs_MpqIXmAT1O",  # 糖醋里脊本脊
        "https://www.douyin.com/user/MS4wLjABAAAA0x-7nbBt6MpoDo9R_777uEMrZldbsqQaiSLQ3aRkyBU",  # 来一两螺蛳粉加小憨梓
        "https://www.douyin.com/user/MS4wLjABAAAAC2mgllQ5qxXmMWGLbH9NhCMCjPjgc8TqYleeYpb5yoY",  # 小瑶郭子🦋-
        "https://www.douyin.com/user/MS4wLjABAAAAXZ4EKoRxZewrzmVzPcgOb4dO0intJ9T_a8z857EbufrQVbfu-gSylzJy-XYWrTGS",  # 霸王龙（聊城第一辣妹）
        "https://www.douyin.com/user/MS4wLjABAAAAs0UUa-ajoRwBio6_62nCz9BWsjb0539dZcIuLQQFkyE",  # 苏落落～
        "https://www.douyin.com/user/MS4wLjABAAAAq5WDPPXnS8z1kkVPhMWDS4LrAnaqzJ8LISdNmA0Gaxs",  # 小如ovo
        "https://www.douyin.com/user/MS4wLjABAAAAcdLig2KyRygH2j4SHpzwahXj7Cin6PDnFhOU4HwIHVx7UU65LAeOfQO267BxUdAZ",  # 方头萱
        "https://www.douyin.com/user/MS4wLjABAAAAnO0aID2cAQrcZphzKcR-zqfdiT_brNm3Ro5eQGeN2sPY7dUbelpshS3iXTrO2C3p",  # 鱼干好吃吗
        "https://www.douyin.com/user/MS4wLjABAAAAegNKr2Ze51EiOE_rL3Mv5YAeP5bHHLX5EGCfWMY8P4GMJWiYjpSYUIt_H0tlAD9S",  # 壳壳有米
        "https://www.douyin.com/user/MS4wLjABAAAAWVwhAs0MqebSA0nqyswZZXZZACn2Z8JOjGXuUlPNeaY",  # 兔丸儿
        "https://www.douyin.com/user/MS4wLjABAAAAyu--axBEGbZvomq18hatQhEN6NkRpr1WyTBa2Am6K7ZghzvKi4FCuTB6LDR83qH7",  # 十一酱
        "https://www.douyin.com/user/MS4wLjABAAAAmTTMKNqxEoFBJAWsvul3Tk3Q6Ajt4s8hGHZ1bKKsaLo",  # Kesally
    ]

    video = Video()
    try:
        video.video_spider(blogger_urls)
    finally:
        video.close_driver()


if __name__ == '__main__':
    main()

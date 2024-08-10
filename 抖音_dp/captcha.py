import time
import ddddocr
import random
from DrissionPage import ChromiumPage
import os
import shutil


class SlideCaptchaSolver:
    def __init__(self):
        self.page = ChromiumPage()

    def delete_img_folder(self):
        """删除img文件夹"""
        folder_name = 'img'
        # 获取当前工作目录
        current_directory = os.getcwd()
        # 构造要删除的文件夹的完整路径
        folder_path = os.path.join(current_directory, folder_name)
        try:
            # 删除文件夹及其内容
            shutil.rmtree(folder_path)
            # print(f"成功删除文件夹: {folder_path}")
        except FileNotFoundError:
            # print(f"文件夹 '{folder_path}' 不存在")
            pass
        except Exception as e:
            print(f"发生错误: {e}")

    def get_distance_by_ddddocr(self):
        """使用ddddocr计算缺口距离"""
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        with open('./img/target.png', 'rb') as f:
            target_bytes = f.read()
        with open('./img/background.png', 'rb') as f:
            background_bytes = f.read()
        res = det.slide_match(target_bytes, background_bytes)
        x_distance = res["target"][0]
        return x_distance

    def get_tracks(self, distance):
        """滑块的运动轨迹"""
        value = round(random.uniform(0.55, 0.75), 2)
        v, t, sum = 0, 0.3, 0
        plus = []
        mid = distance * value
        while sum < distance:
            if sum < mid:
                a = round(random.uniform(2.5, 3.5), 1)
            else:
                a = -round(random.uniform(2.0, 3.0), 1)
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            sum += s
            plus.append(round(s))

        reduce = [-6, -4, -6, -4]
        return {'plus': plus, 'reduce': reduce}

    def move_to_gap(self, slide_ele, tracks):
        """模拟滑块滑动"""
        self.page.actions.hold(f"{slide_ele}")
        for track in tracks['plus']:
            self.page.actions.move(
                offset_x=track,
                offset_y=random.randint(1, 3),
                duration=.1
            )
        time.sleep(0.5)
        self.page.actions.release(f"{slide_ele}")

    def solve_captcha1(self):
        """嵌入式滑块"""
        while True:
            self.delete_img_folder()
            self.page.get("https://castatic.fengkongcloud.cn/pr/v1.0.4/demo.html")
            self.page.ele("@text()=嵌入式(embed)").click()
            self.page.ele('@name=account').input("test")
            self.page.ele('@name=password').input("test")
            # 下载滑块和背景图，target.png 指的是滑块的图片。background.png指的是带有缺口的背景图
            self.page.ele('.shumei_captcha_loaded_img_fg').save(path="./img/", name='target.png')
            self.page.ele('.shumei_captcha_loaded_img_bg').save(path="./img/", name='background.png')
            x_distance = self.get_distance_by_ddddocr()
            # 该网址缺口的计算得除2，因为下载的图片为600 × 300 px ，而在网页上的图片大小为300 × 150 px
            x_distance = x_distance / 2
            # 计算出的轨迹
            trajectory = self.get_tracks(x_distance)
            # 进行移动
            self.move_to_gap(slide_ele=".shumei_captcha_slide_btn_icon sm-iconfont", tracks=trajectory)
            time.sleep(0.2)
            success = self.page.ele('@text()=验证成功', timeout=0.5)
            if success:
                print("验证成功")
                break
            else:
                print("验证失败，正在重试...")
                # 这里可以加入短暂的延时以避免过快重试
                time.sleep(1)
            # 对验证码页面进行截图。
            captcha1 = self.page.ele('#shumei_form_captcha_wrapper')
            if captcha1:
                captcha1.get_screenshot(path="./img/captcha1.png")

    def solve_captcha2(self):
        """浮动式(float)"""
        self.delete_img_folder()
        self.page.get("https://castatic.fengkongcloud.cn/pr/v1.0.4/demo.html")
        self.page.ele("@text()=嵌入式(embed)").click()
        # 必须先输入密码再输入账号，要不然不会弹窗
        self.page.ele('@name=password').input("test")
        self.page.ele('@name=account').input("test")
        # 下载滑块和背景图，target.png 指的是滑块的图片。background.png指的是带有缺口的背景图
        self.page.ele('.shumei_captcha_loaded_img_fg').save(path="./img/", name='target.png')
        self.page.ele('.shumei_captcha_loaded_img_bg').save(path="./img/", name='background.png')
        x_distance = self.get_distance_by_ddddocr()
        # 该网址缺口的计算得除2，因为下载的图片为600 × 300 px ，而在网页上的图片大小为300 × 150 px
        x_distance = x_distance / 2
        # 计算出的轨迹
        trajectory = self.get_tracks(x_distance)
        # 进行移动
        self.move_to_gap(slide_ele=".shumei_captcha_slide_btn_icon sm-iconfont", tracks=trajectory)
        time.sleep(0.2)
        # 对验证码页面进行截图。
        captcha2 = self.page.ele('#shumei_form_captcha_wrapper')
        if captcha2:
            captcha2.get_screenshot(path="./img/captcha2.png")

    def solve_captcha3(self):
        """弹出式(popup)"""
        self.delete_img_folder()
        self.page.get("https://castatic.fengkongcloud.cn/pr/v1.0.4/demo.html")
        self.page.ele("@text()=弹出式(popup)").click()
        self.page.ele('@name=account').input("test")
        self.page.ele('@name=password').input("test")
        # 点击登录，弹出验证码
        self.page.ele('.shumei_login_btn').click()
        # 下载滑块和背景图，target.png 指的是滑块的图片。background.png指的是带有缺口的背景图
        self.page.ele('.shumei_captcha_loaded_img_fg').save(path="./img/", name='target.png')
        self.page.ele('.shumei_captcha_loaded_img_bg').save(path="./img/", name='background.png')
        x_distance = self.get_distance_by_ddddocr()
        # 该网址缺口的计算得除2，因为下载的图片为600 × 300 px ，而在网页上的图片大小为300 × 150 px
        x_distance = x_distance / 2
        # 计算出的轨迹
        trajectory = self.get_tracks(x_distance)
        # 进行移动
        self.move_to_gap(slide_ele=".shumei_captcha_slide_btn_icon sm-iconfont", tracks=trajectory)
        time.sleep(0.2)
        # 对验证码页面进行截图。
        captcha3 = self.page.ele('#shumei_form_captcha_wrapper')
        if captcha3:
            captcha3.get_screenshot(path="./img/captcha3.png")

    def solve_captcha4(self):
        """无图直接滑动"""
        self.delete_img_folder()
        self.page.get("https://castatic.fengkongcloud.cn/pr/v1.0.4/demo.html")
        self.page.ele("@text()=无图直接滑动").click()
        self.page.ele('@name=account').input("test")
        self.page.ele('@name=password').input("test")
        # 点击登录，弹出验证码
        self.page.ele('.shumei_login_btn').click()
        x_distance = (300 - 40)
        # 计算出的轨迹
        trajectory = self.get_tracks(x_distance)
        # 进行移动
        self.move_to_gap(slide_ele=".shumei_captcha_slide_btn_icon sm-iconfont", tracks=trajectory)
        time.sleep(0.2)
        # 对验证码页面进行截图。
        captcha4 = self.page.ele('#shumei_form_captcha_wrapper', timeout=0.5)
        if captcha4:
            captcha4.get_screenshot(path="./img/captcha4.png")

    def solve_captcha5(self):
        """使用bytes传参，不下载验证码图片"""
        self.delete_img_folder()
        self.page.get("https://castatic.fengkongcloud.cn/pr/v1.0.4/demo.html")
        self.page.ele("@text()=嵌入式(embed)").click()
        self.page.ele('@name=account').input("test")
        self.page.ele('@name=password').input("test")
        # 点击登录，弹出验证码
        self.page.ele('.shumei_login_btn').click()
        # 直接获取到验证码滑块和背景图的bytes
        target_bytes = self.page.ele('.shumei_captcha_loaded_img_fg').get_src()
        background_bytes = self.page.ele('.shumei_captcha_loaded_img_bg').get_src()

        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        res = det.slide_match(target_bytes, background_bytes)

        x_distance = res["target"][0] / 2
        trajectory = self.get_tracks(x_distance)
        self.move_to_gap(slide_ele=".shumei_captcha_slide_btn_icon sm-iconfont", tracks=trajectory)
        time.sleep(0.2)
        captcha5 = self.page.ele('#shumei_form_captcha_wrapper')
        if captcha5:
            captcha5.get_screenshot(path="./img/captcha5.png")


# captcha_solver = SlideCaptchaSolver()
# captcha_solver.solve_captcha1()
# captcha_solver.solve_captcha2()
# captcha_solver.solve_captcha3()
# captcha_solver.solve_captcha4()
# captcha_solver.solve_captcha1()

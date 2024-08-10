import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_url_validity(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def check_password_validity(url, key):
    edge_options = webdriver.EdgeOptions()
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
    edge_options.add_argument('--headless')  # 无头模式
    edge_options.add_argument('--disable-gpu')  # 禁用GPU加速
    edge_options.add_argument("disable-cache")  # 禁用缓存
    edge_options.add_argument('disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    edge_options.add_argument('log-level=2')
    driver = webdriver.Edge(options=edge_options)
    driver.get(url)
    try:
        password_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form/div[1]/span/input')
        password_element.click()
        password_element.send_keys(key)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form/div[2]/a').click()
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "常用设置")
        # 密码验证逻辑
        return True
    except NoSuchElementException:
        return False
    finally:
        driver.quit()


def get_url_from_user():
    while True:
        url = input("请输入后台管理URL：")
        if check_url_validity(url):
            return url
        else:
            print("后台管理URL无法访问，请重新输入！")


def get_password_from_user(url):
    while True:
        key = input("请输入后台管理密码：")
        if check_password_validity(url, key):
            return key
        else:
            print("后台管理密码错误，请重新输入！")


def refresh(url, key):
    global driver
    try:
        # 1.打开浏览器
        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
        edge_options.add_argument('--headless')  # 无头模式
        edge_options.add_argument('--disable-gpu')  # 禁用GPU加速
        edge_options.add_argument("disable-cache")  # 禁用缓存
        edge_options.add_argument('disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
        edge_options.add_argument('log-level=2')
        driver = webdriver.Edge(options=edge_options)

        # 2.打开网址
        driver.get(url)
        password_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form/div[1]/span/input')
        password_element.click()
        password_element.send_keys(key)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form/div[2]/a').click()
        time.sleep(1)
        gen_setting = driver.find_element(By.LINK_TEXT, "常用设置")
        gen_setting.click()
        network_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/ul/li[2]/a/i")
        network_button.click()
        time.sleep(2)
        # 3.获取IP地址,执行对应操作
        status = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/ul/li[7]/span[2]").text[:3]
        iptext = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/ul/li[3]/span[2]").text.replace(".", "")
        if (len(iptext) == 7 and (iptext[-1] == iptext[-2] == iptext[-3]) or (iptext[-1] == iptext[-2]) or (
                iptext[-1] or iptext[-2] == "0")) \
                or (
                len(iptext) == 8 and (iptext[4] == iptext[5] == iptext[6] == iptext[7]) or (iptext[4:6] == iptext[6:8])) \
                or (len(iptext) == 9 and (iptext[4] == iptext[5] and iptext[6] == iptext[7] == iptext[8]) or (
                iptext[-1] == iptext[-2] == iptext[-3] == iptext[-4] == iptext[-5])):
            while True:
                if status == "未连接":
                    connection_button = driver.find_element(By.LINK_TEXT, "立即连接")
                    connection_button.click()
                    time.sleep(8)

                element = driver.find_element(By.LINK_TEXT, "断开")
                break_button = element
                break_button.click()
                time.sleep(6)

                connection_button = driver.find_element(By.LINK_TEXT, "立即连接")
                connection_button.click()
                time.sleep(9)

                status = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/ul/li[7]/span[2]").text[:3]
                iptext = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/ul/li[3]/span[2]").text.replace(".", "")
                if status == "拨号成":
                    print("{}功：".format(status), iptext[:2] + '.' + iptext[2:4] + '.' + iptext[4:6] + '.' + iptext[6:])
                else:
                    print(status, iptext)

                if len(iptext) == 7:
                    if (iptext[-1] == iptext[-2] == iptext[-3]) or (iptext[-1] == iptext[-2]) or (
                            iptext[-1] or iptext[-2] == "0"):
                        print("IP地址已完美！")
                        break
                elif len(iptext) == 8:
                    if (iptext[4] == iptext[5] == iptext[6] == iptext[7]) or (iptext[4:6] == iptext[6:8]) \
                            or (iptext[4:8 == "3051" or "3040" or "1217" or "1117"]) or (
                            iptext[5] and iptext[7] == "0"):
                        print("IP地址已完美！")
                        break
                elif len(iptext) == 9:
                    if (iptext[4] == iptext[5] and iptext[6] == iptext[7] == iptext[8]) or (
                            iptext[-1] == iptext[-2] == iptext[-3] == iptext[-4] == iptext[-5]):
                        print("IP地址已完美！")
                        break
        else:
            print("IP地址已完美！")
        driver.quit()
        input("按任意键退出")
    except:
        print("IP地址获取错误，正在重试！请不要关闭窗口！")
        print("如果多次运行出错，请关闭重新运行！")
        driver.quit()
        refresh(url, key)


def main():
    print("============================")
    print("Powered By Viper3")
    print("Copyright©2023.04")
    print("博客地址：viper3.top")
    print("云盘地址：cloud.viper3.top")
    print("============================")
    print("您的后台管理URL为（例：miwifi默认为'http://192.168.31.1'）")
    url = get_url_from_user()
    key = get_password_from_user(url)

    # 执行随后的操作
    refresh(url, key)


if __name__ == "__main__":
    main()

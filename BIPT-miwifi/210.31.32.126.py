import time
from selenium import webdriver
from selenium.webdriver.common.by import By  # 控制浏览器模拟鼠标动作模块
from selenium.webdriver.edge.service import Service  # selenium模块启动edge浏览器服务


# 判断元素是否存在
def elementExit(browsers, by, ele):
    try:
        browsers.find_element(by, ele)
        return True
    except:
        return False


edgedriver = Service('msedgedriver.exe')
edgedriver.start()
browser = webdriver.Remote(edgedriver.service_url)


def loginNetwork():
    networkURL = "http://210.31.32.126/"
    browser.get(networkURL)

    if elementExit(browser, By.ID, "login-account"):  # 判断按钮是否为"登录"二字
        # 输入账号
        user = browser.find_element(By.ID, "username")
        user.click()
        time.sleep(1)
        user.send_keys("2020311228")

        # 输入密码
        password = browser.find_element(By.ID, "password")
        password.click()
        time.sleep(1)
        password.send_keys("Shxy170317")  # Shxy145211

        # 点击登录
        login = browser.find_element(By.ID, "login-account")
        login.click()
        time.sleep(1)
        browser.execute_script("window.open('www.baidu.com','_blank');")
        browser.switch_to.window(browser.window_handles[1])
    else:
        logout = browser.find_element(By.ID, "logout")
        logout.click()
        browser.execute_script("window.open('https://www.baidu.com','_blank');")
        browser.switch_to.window(browser.window_handles[1])
        # 点击注销


loginNetwork()

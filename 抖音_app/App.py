import time

from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {
    'platformName': 'Android',
    'deviceName': '62c81deb',
    'platformVersion': '13',
    'appPackage': 'com.ss.android.ugc.aweme',
    'appActivity': 'com.ss.android.ugc.aweme.splash.SplashActivity',
    'noReset': True
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 启动app


time.sleep(3)
x = driver.get_window_size()['width']
y = driver.get_window_size()['height']

x1 = int(x * 0.9)
x2 = int(x * 0.1)
y1 = int(y * 0.5)
y2 = int(y * 0.5)
# 模拟滑动
time.sleep(1)
driver.swipe(x1, y1, x2, y2)

name = driver.find_element(By.ID, 'com.ss.android.ugc.aweme:id/o3b').text
print(name)


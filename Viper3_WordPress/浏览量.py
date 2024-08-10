import time
import threading
from selenium import webdriver
from selenium.webdriver.edge.service import Service


def get():
    p = ['917', '885', '871', '857', '828', '805', '791', '616', '613', '583', '764', '575', '738', '92', '773',
         '647', '728', '650', '556', '917', '907', '885', '871', '857', '828', '805', '791', '616', '613', '583', '764',
         '575', '738', '92', '773', '647', '728', '650', '556', '917', '907', '885', '871', '857', '828', '805', '791',
         '616', '613', '583', '764', '575', '738', '92', '773', '647', '728', '650', '556', '917', '907', '885', '871',
         '857', '828', '805', '791', '616', '613', '583', '764', '575', '738', '92', '773', '647', '728', '650', '556']
    service = Service('msedgedriver.exe')
    service.start()
    browser = webdriver.Remote(service.service_url)
    count = 0
    while count != 100:
        for i in p:
            url = "https://rfzf.top/?p={}".format(str(i))
            browser.get(url)
            time.sleep(3)
        count += 1
    browser.close()


def index():
    url = "https://rfzf.top/"
    service = Service('msedgedriver.exe')
    service.start()
    browser = webdriver.Remote(service.service_url)
    browser.get(url)
    time.sleep(1)
    count = 0
    while count != 5000:
        browser.refresh()
        time.sleep(1)
        count += 1
    browser.close()


threads = []
# 文章
t0 = threading.Thread(target=get, args=())
t1 = threading.Thread(target=get, args=())
t2 = threading.Thread(target=get, args=())
t3 = threading.Thread(target=get, args=())
t4 = threading.Thread(target=get, args=())
t5 = threading.Thread(target=get, args=())
t6 = threading.Thread(target=get, args=())
t7 = threading.Thread(target=get, args=())
t8 = threading.Thread(target=get, args=())
t9 = threading.Thread(target=get, args=())
# 首页
t10 = threading.Thread(target=index, args=())
t11 = threading.Thread(target=index, args=())

threads.append(t0)
threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)
threads.append(t5)
threads.append(t6)
threads.append(t7)
threads.append(t8)
threads.append(t9)
threads.append(t10)
threads.append(t11)


if __name__ == '__main__':
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.perf_counter()
    print("12线程访问量刷取共耗时{}秒，退出线程".format(end-start))
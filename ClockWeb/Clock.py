import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pymysql
import logging

yes = 0


# 判断元素是否存在
def elementExit(browsers, by, ele):
    try:
        browsers.find_element(by, ele)
        return True
    except:
        return False


# 获取当前时间 格式为:2022-10-14 23:dy_17:32
def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 日志
def logger_config(log_path, logging_name):
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 为logger对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


# 打卡
def Clock(userid, idPassword):
    # 登录校园网
    edgedriver = Service('msedgedriver.exe')
    edgedriver.start()
    browser = webdriver.Remote(edgedriver.service_url)
    networkURL = "http://210.31.32.126/"
    browser.get(networkURL)
    browser.refresh()
    time.sleep(2)
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
    else:
        pass
    global yes

    # 访问网站并清除cookie
    url = "https://mapp.bipt.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fmapp.bipt.edu.cn%2Fuc%2Fapi%2Foauth%2Findex%3Fredirect%3Dhttps%3A%2F%2Fjk.bipt.edu.cn%2Fapi%2Flogin%2Fpages-index-index%3Flogin%3D1%26appid%3D200211214214852461%26state%3DSTATE"
    browser.get(url)
    browser.delete_all_cookies()

    # 输入账号
    User = browser.find_elements(By.CSS_SELECTOR, "[placeholder='账号']")
    time.sleep(1)
    User[0].click()
    time.sleep(1)
    User[0].send_keys(userid)
    time.sleep(1)

    # 输入密码
    password = browser.find_elements(By.CSS_SELECTOR, "[placeholder='密码']")
    time.sleep(1)
    password[0].click()
    time.sleep(1)
    password[0].send_keys(idPassword)
    time.sleep(1)

    # 点击登录
    login = browser.find_element(By.CLASS_NAME, "btn")
    time.sleep(1)
    login.click()
    time.sleep(10)

    # 判断今日是否打过卡
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    state = soup.select(
        "body > uni-app > uni-page > uni-page-wrapper > uni-page-body > uni-scroll-view > div > div > div > uni-view.content > uni-view:nth-child(4) > uni-view.btn-over")
    if len(state) == 0:
        # 选择选项
        no_btn = browser.find_elements(By.CSS_SELECTOR, "[class='u-radio__label']")
        no_btn[0].click()
        time.sleep(1)
        no_btn[3].click()
        time.sleep(1)
        no_btn[9].click()
        time.sleep(1)
        no_btn[11].click()
        time.sleep(1)
        no_btn[36].click()
        # 获取位置信息
        local = browser.find_elements(By.CSS_SELECTOR, "[class='uni-input-input']")
        time.sleep(1)
        local[6].click()
        time.sleep(10)

        # 提交信息
        submit = browser.find_element(By.CLASS_NAME, "btn")
        time.sleep(1)
        submit.click()
        time.sleep(3)
    else:
        yes = 1

    # 关闭浏览器
    browser.close()


# 发送打卡反馈邮件
def sendEmail(msg, reEmail, Server, Sender, Password):
    global smtp
    logger = logger_config(log_path='log.txt', logging_name='sendEmail')
    # 发送邮件服务器地址
    smtp_server = Server
    # 发件方邮箱
    sender = Sender
    # 发件方密码
    smtpPassword = Password
    # 收件方邮箱
    receiver = reEmail
    # 邮件标题
    time_list = time.strftime("%D", time.localtime()).split("/")
    time_day = "2022-" + time_list[0] + "-" + time_list[1]
    subject = '{} 自动打卡反馈'.format(time_day)
    # 邮件内容
    mail_msg = msg
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，html 设置文本格式为html格式  第三个 utf-8 设置编码
    message = MIMEText(mail_msg, 'plain', 'utf-8')
    # 发送地址
    message['From'] = sender
    # 接受地址
    message['To'] = receiver
    # 邮件标题
    message['Subject'] = Header(subject, 'utf-8')
    try:
        # 创建SMTP对象
        smtp = smtplib.SMTP()
        # 连接服务器
        smtp.connect(smtp_server)
        # 登录邮箱账号
        smtp.login(sender, smtpPassword)
        # 发送账号信息
        smtp.sendmail(sender, receiver, message.as_string())
        # print('{} Info: 邮箱: {} 打卡反馈邮件发送成功'.format(getTime(), reEmail))
    except smtplib.SMTPException:
        logger.error("打卡反馈邮件新发送失败")
    finally:
        # 关闭
        smtp.quit()


# 获取需要打卡的用户信息
def getUserInfo():
    logger = logger_config(log_path='log.txt', logging_name='getUserInfo')
    conn = pymysql.connect(host='10.10.40.20', user='clock_info', password='clock_info', db='clock_info', port=3306,
                           charset='utf8')
    cursor = conn.cursor()
    sql = 'select * from user'
    cursor.execute(sql)
    data = list(cursor.fetchall())
    userid_list = []
    password_list = []
    reEmail_list = []
    smtpServer_list = []
    smtpSender_list = []
    smtpPassword_list = []
    for i in data:
        # 判断是否过期，如果过期则不添加到打卡名单中。
        if str(i[6]) < getTime():
            logger.info("用户: {} 已到期，请提醒续费！".format(i[0]))
        else:
            userid_list.append(i[0])
            password_list.append(i[1])
            reEmail_list.append(i[2])
            smtpServer_list.append(i[3])
            smtpSender_list.append(i[4])
            smtpPassword_list.append(i[5])
    conn.close()
    logger.info("用户信息获取完成！")
    return userid_list, password_list, reEmail_list, smtpServer_list, smtpSender_list, smtpPassword_list


# 获取管理员邮箱信息
def getAdminInfo():
    logger = logger_config(log_path='log.txt', logging_name='getAdminInfo')
    conn = pymysql.connect(host='10.10.40.20', user='clock_info', password='clock_info', db='clock_info', port=3306,
                           charset='utf8')
    cursor = conn.cursor()
    sql = 'select * from admin'
    cursor.execute(sql)
    data = cursor.fetchall()
    data = list(data)
    adminEmail_list = []
    for i in data:
        adminEmail_list.append(i[0])
    conn.close()
    logger.info("管理员信息获取完成！")
    return adminEmail_list


# main方法
def main():
    global uid
    global reEml
    while True:
        start_time = time.time()
        print("------自动打卡程序将在10s后开始运行，运行期间请勿进行操作------")
        time.sleep(7)
        print("------自动打卡程序将在5s后开始运行，运行期间请勿进行操作-------")
        time.sleep(3)
        logger = logger_config(log_path='log.txt', logging_name='main')
        # 获取管理员邮箱
        adminEmail_list = getAdminInfo()
        # 获取用户和smtp服务的信息
        userid_list, password_list, reEmail_list, smtpServer_list, smtpSender_list, smtpPassword_list = getUserInfo()
        conn = pymysql.connect(host='10.10.40.20', user='clock_info', password='clock_info', db='clock_info', port=3306,
                               charset='utf8')
        cursor = conn.cursor()
        try:
            # 遍历所有用户信息
            for i in range(len(userid_list)):
                uid = userid_list[i]
                pwd = password_list[i]
                reEml = reEmail_list[i]
                smtpServer = smtpServer_list[i]
                smtpSender = smtpSender_list[i]
                smtpPassword = smtpPassword_list[i]
                # 第一次为打卡，第二次为打卡是否成功做确认
                for j in range(0, 3):
                    Clock(uid, pwd)
                    if yes == 1:  # 判断是否有今日已提交
                        logger.info("用户: {} 自动打卡成功".format(uid))
                        sendEmail("用户: {} 您好，今日打卡成功！".format(uid), reEml, smtpServer, smtpSender, smtpPassword)
                        logger.info('邮箱: {} 打卡反馈邮件发送成功'.format(reEml))
                        # 打卡结果写入数据库
                        sql = 'insert into clocklog (datetime, userID, feedback) values (\'{}\',\'{}\',\'{}\')'.format(
                            getTime(), uid, "成功")
                        cursor.execute(sql)
                        conn.commit()
                        logger.info("用户: {} 打卡结果已写入数据库".format(uid))
                        break
        except Exception as ex:
            logger.error("{}".format(ex).strip())
            time.sleep(1)
            logger.error("用户: {} 打卡失败, 请及时处理".format(uid))
            # 发送错误邮件给管理员
            for reEmail in adminEmail_list:
                sendEmail("{} Error: {} 打卡失败, 请及时处理".format(getTime(), uid), reEmail, "smtp.exmail.qq.com",
                          "mysheep@mysheep.cc", "Yangjiaji0323")
                # 打卡结果数据库
                sql = 'insert into clocklog (datetime, userID, feedback) values (\'{}\',\'{}\',\'{}\')'.format(
                    getTime(), uid, "失败")
                cursor.execute(sql)
                conn.commit()
                logger.info("用户: {} 打卡结果已写入数据库".format(uid))

        time.sleep(1)
        conn.close()
        print("------自动打卡程序运行结束 可以进行操作------")
        print("---------请勿关闭此窗口---------")
        end_time = time.time()
        difference_time = end_time - start_time
        time.sleep(86400 - difference_time)


if __name__ == "__main__":
    main()

import time

from wxauto import *
# 获取当前微信客户端
wx = WeChat()
# 向某人发送消息
while True:
    wx.SendMsg('那咋了', '盾宝🐰（玉桂狗版')
    time.sleep(0.2)
    break

import cv2
from matplotlib import pyplot as plt
import re
import xml
from xml.dom import minidom
import os


# 绘制图像
def getFont():
    temp_x = 0
    temp_y = 0
    flag = 0
    data = []
    xmlfilepath_find = os.path.abspath("./chuLi/data/e3dfe524.xml")  # 获取xml
    # 接下来要打开他，获取每一个数字的画法,打开这个xml
    domobj_find = xml.dom.minidom.parse(xmlfilepath_find)
    elementobj_find = domobj_find.documentElement
    # 获取 ttglyph下的所有内容
    subElementObj = elementobj_find.getElementsByTagName("TTGlyph")
    for i in range(len(subElementObj)):
        rereobj = re.compile(r"name=\"(.*)\"")
        find_list = rereobj.findall(str(subElementObj[i].toprettyxml()))
        data.append(str(subElementObj[i].toprettyxml()).replace(find_list[0], '').replace("\n", ''))

    for j in range(1, 11):
        data[j] = data[j].split('pt ')
        first_point = True  # 初始化标志，用于标记是否是每个数字的第一个点
        for i in range(1, len(data[j])):
            temp = re.findall('=.*?/>', data[j][i])
            temp = temp[0].split('\"')
            print()
            if temp[5] == '1' or temp[5] == '0':
                x = int(temp[1])
                y = int(temp[3])
                if first_point:
                    first_x, first_y = x, y  # 存储第一个点的坐标
                    first_point = False
                    temp_x = x
                    temp_y = y
                else:
                    plt.scatter(x, y, c='r')
                    plt.plot([x, temp_x], [y, temp_y], c='r')
                temp_x, temp_y = x, y  # 更新前一个点的坐标
        if not first_point:  # 如果至少绘制了一个点
            plt.plot([temp_x, first_x], [temp_y, first_y], c='r')  # 绘制从最后一个点回到第一个点的线

        # plt.show()  # 保存图片不能show
        cv2.waitKey()
        plt.savefig('./chuLi/img/' + str(j - 1) + '.png')
        plt.close()


# 灰度化
def grayImg():
    temp = "./chuLi/img/{}.png"
    for i in range(0, 10):
        # print(temp.format(str(i)))
        img = cv2.imread(temp.format(str(i)))
        # 灰度化
        GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 保存
        cv2.imwrite(temp.format(str(i)), GrayImage)
        # 裁剪
    for i in range(0, 10):
        img = cv2.imread(temp.format(str(i)).format(str(i)))
        cropped = img[60:420, 81:575]  # 裁剪坐标为[y0:y1, x0:x1]
        # cv2.imshow(str(i)+'.png',cropped)
        cv2.imwrite(temp.format(str(i)), cropped)
        # cv2.waitKey()


# 降采样
def resizeA():
    temp = "./chuLi/img/{}.png"
    for i in range(0, 10):
        path = temp.format(str(i))
        pic_1 = cv2.imread(path)
        pic = cv2.resize(pic_1, (32, 32), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, pic)


getFont()
# grayImg()
# resizeA()

from lxml import etree
from fontTools.ttLib import TTFont
import cv2
from matplotlib import pyplot as plt
import re
import xml
from xml.dom import minidom
import os
import PIL
import imagehash
import csv

woffPath = "./chuLi/data/e3dfe524.woff"
xmlPath = './chuLi/data/e3dfe524.xml'
imgPath = "./chuLi/img/{}.png"


def woffTOxml():
    font = TTFont(woffPath)  # 打开woff字体
    font.saveXML(xmlPath)  # 转存为xml方便查看


# 绘制图像
def getFont():
    tree = etree.parse('./chuLi/data/e3dfe524.xml')
    TTGlyphList = tree.xpath('/ttFont/glyf/TTGlyph')
    count = 0
    for TTGlyph in TTGlyphList:
        if 'uni' in TTGlyph.xpath('./@name')[0]:
            PointCoordinates = TTGlyph.xpath('./contour/pt/@x|./contour/pt/@y')
            first_point = True  # 初始化标志，用于标记是否是每个数字的第一个点
            for Point in range(0, len(PointCoordinates), 2):
                x = int(PointCoordinates[Point])
                y = int(PointCoordinates[Point + 1])
                if first_point:
                    # 存储第一个点，为了最后一个点和第一个点的连接
                    first_x, first_y = x, y  # 存储第一个点的坐标
                    first_point = False
                    # 因为第一个点不需要位置，所以直接将坐标标记为上一个点。
                    temp_x = x
                    temp_y = y
                    plt.scatter(x, y, c='r')
                else:
                    plt.scatter(x, y, c='r')
                    plt.plot([x, temp_x], [y, temp_y], c='r')
                temp_x, temp_y = x, y  # 更新前一个点的坐标
            if not first_point:  # 如果至少绘制了一个点
                plt.plot([temp_x, first_x], [temp_y, first_y], c='r')  # 绘制从最后一个点回到第一个点的线
            # plt.show()
            plt.savefig(f'./test/{count}.png')
            plt.close()
            count += 1


# 灰度化
def grayImg():
    temp = imgPath
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
        cv2.imwrite(temp.format(str(i)), cropped)


# 降采样
def resizeA():
    temp = imgPath
    for i in range(0, 10):
        path = temp.format(str(i))
        pic_1 = cv2.imread(path)
        pic = cv2.resize(pic_1, (32, 32), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, pic)


# 获取图片指纹
def phash():
    hash = []
    temp = "./chuLi/img/{}.png"
    for i in range(0, 10):
        img = PIL.Image.open(temp.format(str(i)))
        a = imagehash.phash(img)
        hash.append(str(a))
        with open('./chuLi/data/cmphash.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([a, i])


def campareDIS(cmphash, datafont):
    basehashFile = open('./data/basehash.csv', 'r').read()
    basehashFile = basehashFile.split('\n')
    # 删除空值
    basehashFile = list(filter(None, basehashFile))
    basehashList = []
    for k in basehashFile:
        basehash, num = k.split(',')
        basehashList.append((basehash, num))
    flag = 1
    this = 0
    for i in range(0, 10):
        hamming_distance = 0
        tempA = int(cmphash, 16)
        temp = int(basehashList[i][0], 16)
        s = str(bin(temp ^ tempA))
        for j in range(2, len(s)):
            if int(s[j]) == 1:
                hamming_distance += 1
        # print('与' + basehashList[i][1] + '的汉明距离为', hamming_distance)
        if flag == 1:
            hamming_distanceA = hamming_distance
            flag = flag + 1
            continue
        if (hamming_distanceA > hamming_distance):
            hamming_distanceA = hamming_distance
            this = int(basehashList[i][1])
    return datafont, this


def getNumCode():
    tree = etree.parse(xmlPath)
    numCodeList = tree.xpath('/ttFont/glyf/TTGlyph/@name')
    removeList = []
    for index in range(len(numCodeList)):
        if 'uni' not in numCodeList[index]:
            removeList.append(index)
    for j in removeList[::-1]:
        numCodeList.pop(j)
    return numCodeList


os.remove('./chuLi/data/cmphash.csv')
woffTOxml()
getFont()
grayImg()
resizeA()
phash()

numCodeList = getNumCode()
cmphashFile = open('./chuLi/data/cmphash.csv', 'r').read()
cmphashFile = cmphashFile.split('\n')
# # 删除空值
cmphashFile = list(filter(None, cmphashFile))
cmphashList = []
for k in cmphashFile:
    cmphash, num = k.split(',')
    cmphashList.append((cmphash, num))
dic = []
for ii in range(len(cmphashList)):
    numCode, this = campareDIS(cmphashList[ii][0], numCodeList[ii])
    print(f'{numCode}当前字识别为{this}')
    dic.append((numCode.replace('uni', '&#x').lower() + ";", this))
print(dic)

import numpy as np
from lxml import etree
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from PIL import Image, ImageFilter
import pandas as pd


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
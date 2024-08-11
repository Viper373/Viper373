
def campareDIS(basehashList, cmphash, datafont):
    flag = True
    this = 0
    for i in range(0, 10):
        hamming_distance = 0
        # 将16进制转为10进制
        tempA = int(cmphash, 16)
        temp = int(basehashList[i][0], 16)
        # 计算tempA和temp的异或值
        s = str(bin(temp ^ tempA))
        # 计算汉明距离
        for j in range(2, len(s)):
            if int(s[j]) == 1:
                hamming_distance += 1
        print('与' + basehashList[i][1] + '的汉明距离为', hamming_distance)

        # 存储中间变量，记录距离最小的数
        if flag:
            hamming_distanceA = hamming_distance
            flag = False
            continue
        if (hamming_distanceA > hamming_distance):
            hamming_distanceA = hamming_distance
            this = int(basehashList[i][1])

    return datafont, this


basehashFile = open('./data/basehash.csv', 'r').read()
basehashFile = basehashFile.split('\n')
# 删除空值
basehashFile = list(filter(None, basehashFile))
basehashList = []
for k in basehashFile:
    basehash, num = k.split(',')
    basehashList.append((basehash, num))
print(basehashList)

datafont, this = campareDIS(basehashList, 'f9cd30ba609f9588', 'uniEB19')
print(f'{datafont}当前数字识别为', this)

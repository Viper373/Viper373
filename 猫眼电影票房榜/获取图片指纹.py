# 使用imagehash库中的phash，
# 感知hash去获取每一张图片的指纹
# 然后写入的csv中，这样这些图片信息就会保存为10个16进制数字，而这10个16进制数字就代表了这些图片的所有特征
import PIL
import imagehash
import csv


def phash():
    hash = []
    temp = "./chuLi/img/{}.png"
    for i in range(0, 10):
        img = PIL.Image.open(temp.format(str(i)))
        a = imagehash.phash(img)
        hash.append(str(a))
        with open('./chuLi/data/imgHash.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([a, i])
        print(a)

phash()

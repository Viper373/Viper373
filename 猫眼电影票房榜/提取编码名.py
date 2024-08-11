from lxml import etree


tree = etree.parse('./chuLi/data/e3dfe524.xml')
numCodeList = tree.xpath('/ttFont/glyf/TTGlyph/@name')
removeList = []
for index in range(len(numCodeList)):
    if 'uni' not in numCodeList[index]:
        removeList.append(index)

for j in removeList[::-1]:
    numCodeList.pop(j)

print(numCodeList)

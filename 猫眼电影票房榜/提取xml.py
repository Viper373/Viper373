from fontTools.ttLib import TTFont
font = TTFont("./chuLi/data/75e5b39d.woff")  #打开woff字体
font.saveXML('./chuLi/data/75e5b39d.xml')   #转存为xml方便查看
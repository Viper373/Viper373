from BlogContentInfo import BlogContentInfo


def main():
    """
    主函数
    :return:
    """
    # 实例化类
    BCI = BlogContentInfo("https://viper3.top/")
    # 获取页码链接
    pageURL_List = BCI.getPageURL()
    print("一共有{}页，链接分别是 ↓↓↓ \n {}".format(len(pageURL_List), pageURL_List))
    # 获取文章链接
    paperURL_List = BCI.getPaperURL()
    print("一共有{}篇文章，链接分别是 ↓↓↓".format(len(paperURL_List)))
    for paperURL in paperURL_List:
        # 输出文章链接
        print(paperURL)
        # getContent()获取文章内容，输出文章内容
        print(BCI.getContent(paperURL, True))


if __name__ == '__main__':
    main()

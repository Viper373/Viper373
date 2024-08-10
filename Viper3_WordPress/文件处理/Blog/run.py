from BlogImgInfo import BlogImgInfo


def main():
    """
    主函数
    :return:
    """
    # 实例化类
    BII = BlogImgInfo("https://viper3.top/")
    # 获取页码链接ee
    pageURL_List = BII.getPageURL()
    print("一共有{}页，链接分别是 ↓↓↓ \n {}".format(len(pageURL_List), pageURL_List))
    # 获取文章链接
    paperURL_List = BII.getPaperURL()
    print("一共有{}篇文章，链接分别是 ↓↓↓".format(len(paperURL_List)))
    image_folder = "./BlogImg"  # 设置图片保存的本地文件夹路径
    for paperURL in paperURL_List:
        # 调用saveImagesToLocal方法来保存文章图片
        print("-------文章链接：{}".format(paperURL))
        BII.saveImagesToLocal(paperURL, image_folder)  # 保存文章图片到指定文件夹
    print("所有文章图片下载完成")


if __name__ == '__main__':
    main()

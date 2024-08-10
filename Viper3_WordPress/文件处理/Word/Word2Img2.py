import os
import docx
import re
import time


def words2imgs2(word_files_path, output_path):
    # 检查输出路径是否存在，如果不存在则创建
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 遍历所有Word文件
    for root, _, files in os.walk(word_files_path):
        for file in files:
            if file.endswith(".docx"):
                word_path = os.path.join(root, file)
                # 创建以Word文件名命名的目录
                word_folder_name = os.path.splitext(file)[0]
                word_output_path = os.path.join(output_path, word_folder_name)

                # 检查目录是否存在，如果不存在则创建
                if not os.path.exists(word_output_path):
                    os.makedirs(word_output_path)

                # 提取Word文件中的图片
                word2img2(word_path, word_output_path)


def word2img2(word_path, result_path):
    doc = docx.Document(word_path)
    dict_rel = doc.part._rels
    for rel in dict_rel:
        rel = dict_rel[rel]
        if "image" in rel.target_ref:
            img_name = re.findall("/(.*)", rel.target_ref)[0]
            timestamp = int(time.time())  # 获取当前时间戳
            img_name = f'{timestamp}_{img_name}'  # 使用时间戳作为图片名称
            with open(os.path.join(result_path, img_name), "wb") as f:
                f.write(rel.target_part.blob)


def main():
    print("============================")
    print("技术支持由Viper3强力驱动")
    print("Copyright©2023.09.26")
    print("博客地址：viper3.top")
    print("云盘地址：cloud.viper3.top")
    print("============================")
    wordFiles = input("请输入存放word文档的目录路径：")
    WordImgs = input("请输入存放word文档中图片的目录路径：")
    words2imgs2(
        fr'{wordFiles}',
        fr"{WordImgs}")


if __name__ == '__main__':
    main()

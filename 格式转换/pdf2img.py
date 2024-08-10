import fitz  # PyMuPDF


# 定义一个函数来将PDF文件转换为高分辨率图片
def pdf_to_high_res_images(pdf_path, output_folder, zoom_x=3.0, zoom_y=3.0):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)
    # 遍历每一页
    for page_num in range(len(pdf_document)):
        # 获取PDF页面
        page = pdf_document.load_page(page_num)
        # 设置缩放比例
        mat = fitz.Matrix(zoom_x, zoom_y)
        # 将页面转换为图像
        pix = page.get_pixmap(matrix=mat)
        # 定义输出的图像路径
        output_image_path = f"{output_folder}/学信档案证明.png"
        # 保存图像
        pix.save(output_image_path)
    print("PDF已成功转换为高分辨率图片并保存。")


# 输入PDF文件路径
pdf_path = r"O:\北京石油化工学院\2024春（毕业）\就业\应聘材料\教育部学历证书电子注册备案表_张今朝.pdf"
# 输出图片的文件夹路径
output_folder = r"O:\北京石油化工学院\2024春（毕业）\就业\应聘材料"

# 调用函数将PDF转换为高分辨率图片
pdf_to_high_res_images(pdf_path, output_folder)
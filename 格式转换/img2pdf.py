from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# 定义一个函数来将图片转换为PDF
def images_to_pdf(image_paths, pdf_path):
    # 创建一个canvas对象，并设置PDF页面大小
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    for image_path in image_paths:
        # 打开图片
        image = Image.open(image_path)
        # 获取图片的宽度和高度
        img_width, img_height = image.size
        # 计算图片缩放比例以适应PDF页面
        ratio = min(width / img_width, height / img_height)
        img_width = int(img_width * ratio)
        img_height = int(img_height * ratio)
        # 将图片添加到PDF页面
        c.drawImage(image_path, 0, height - img_height, img_width, img_height)
        # 创建新的PDF页面
        c.showPage()

    # 保存PDF文件
    c.save()


# 图片路径列表
image_paths = [r"O:\北京石油化工学院\2024春（毕业）\就业\体检\张今朝体检表正面.jpg", r"O:\北京石油化工学院\2024春（毕业）\就业\体检\张今朝体检表反面.jpg"]
# 输出PDF文件路径
pdf_path = r"O:\北京石油化工学院\2024春（毕业）\就业\体检\张今朝体检报告.pdf"

# 调用函数将图片转换为PDF
images_to_pdf(image_paths, pdf_path)

import os
from os.path import basename, join
from pathlib import Path

from docx import ImagePart, Document
from pofile import get_files, mkdir
from poprogress import simple_progress
from win32com.client import constants, gencache
from tqdm import tqdm


class MainWord():

    def __init__(self):
        self.app = 'Word.Application'

    def docx2pdf(self, path, output_path, docxSuffix=".docx", pdfSuffix='.pdf'):
        waiting_covert_docx_files = get_files(path, suffix=docxSuffix)
        if waiting_covert_docx_files:
            print(f'一共有{len(waiting_covert_docx_files)}个docx文件')
            for i, docx_file in simple_progress(enumerate(waiting_covert_docx_files)):
                abs_output_path = Path(output_path).absolute()
                mkdir(abs_output_path)
                if not abs_output_path.exists():
                    abs_output_path.mkdir()
                abs_single_docx_path = Path(docx_file).absolute()
                print(f'正在转换的是第 {str(i + 1)} 个，文档名字是： {abs_single_docx_path}')
                abs_pdf_path = abs_output_path / (abs_single_docx_path.stem + pdfSuffix)
                self.createpdf(str(abs_single_docx_path), str(abs_pdf_path))

    def createpdf(self, wordPath, pdfPath):
        word_app = gencache.EnsureDispatch(self.app)
        word_app.Visible = False  # 是否可视化
        doc = word_app.Documents.Open(wordPath, ReadOnly=1)
        # 转换方法
        doc.ExportAsFixedFormat(pdfPath, constants.wdExportFormatPDF)
        # word_app.Quit() #不注释，不能批量转换，必须注释

    def merge4docx(self, input_path, output_path, new_word_name):
        abs_input_path = Path(input_path).absolute()  # 相对路径→绝对路径
        abs_output_path = Path(output_path).absolute()  # 相对路径→绝对路径
        mkdir(abs_output_path)
        save_path = abs_output_path / new_word_name
        print('-' * 10 + '开始合并!' + '-' * 10)
        word_app = gencache.EnsureDispatch(self.app)  # 打开word程序
        word_app.Visible = False  # 是否可视化
        folder = Path(abs_input_path)
        waiting_files = [path for path in folder.iterdir()]
        output_file = word_app.Documents.Add()  # 新建合并后的文档
        for single_file in tqdm(waiting_files, colour='green'):
            output_file.Application.Selection.InsertFile(single_file)  # 拼接文档
        output_file.SaveAs(str(save_path))  # 保存
        output_file.Close()
        print('-' * 10 + '合并完成!' + '-' * 10)

    def doc2docx(self, input_path, output_path, docSuffix='.doc', type_id=16):
        """
        doc转docx
        :param input_path:
        :param output_path:
        :param docSuffix:
        :param type_id:
        :return:
        """
        self.convert4word(type_id, input_path, output_path, docSuffix)

    def docx2doc(self, input_path, output_path='./', docSuffix='.docx', type_id=0):
        """
        docx转doc
        :param input_path:
        :param output_path:
        :param docSuffix:
        :param type_id:
        :return:
        """
        self.convert4word(type_id, input_path, output_path, docSuffix)

    def convert4word(self, type_id, input_path, output_path, docSuffix):
        """

        :param type_id: 16-docx,0-doc
        :return:
        """
        abs_input_path = Path(input_path).absolute()
        exsit, abs_output_path = mkdir(output_path)
        word_file_list = get_files(abs_input_path, suffix=docSuffix)
        out_suffix = '.doc' if type_id == 0 else '.docx'
        for word_file in simple_progress(word_file_list):
            # self.convert4word(type_id, abs_input_path, abs_output_path)
            word_app = gencache.EnsureDispatch(self.app)  # 打开word程序
            word_app.Visible = False  # 是否可视化
            # 源文件
            doc = word_app.Documents.Open(str(word_file), ReadOnly=1)
            # 生成的新文件
            output_word_name = os.path.join(abs_output_path, Path(word_file).stem) + out_suffix
            doc.SaveAs(output_word_name, type_id)
            doc.Close()
        # word.Quit()

    def docx4imgs(self, word_path, img_path):
        """
        从wotd里，提取图片
        :author Wang Peng
        :param word_path:
        :param img_path:
        :return:
        """
        doc_obj = Document(word_path)
        for rel in doc_obj.part.rels.values():  # 遍历文档中的所有关联对象
            if "image" in rel.reltype:  # 找到关联类型为图片的对象
                img_part = rel.target_part
                if not isinstance(img_part, ImagePart):
                    continue
                output_dir = Path(img_path) / Path(word_path).stem
                mkdir(output_dir)
                save_path = join(output_dir, basename(img_part.partname))  # 获取默认文件名image1
                with open(save_path, "wb") as img_file:
                    img_file.write(img_part.blob)

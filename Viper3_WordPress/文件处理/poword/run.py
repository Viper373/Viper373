import merge

if __name__ == '__main__':
    word = merge.MainWord()
    word.merge4docx(input_path=r'O:\北京石油化工学院\2022春\数据采集与预处理实践\博客\文件处理\poword\files',
                    output_path=r'O:\北京石油化工学院\2022春\数据采集与预处理实践\博客\文件处理\poword\output',
                    new_word_name='merge.docx')

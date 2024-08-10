# 🐲本项目简介
League of Legends Pro League 综合分析结果预测
## 🐬简介
该项目是一个数据采集、预处理和分析的项目，主要针对英雄联盟（League of Legends）职业联赛（LPL）的数据进行处理和分析。项目分为两部分，分别是数据采集与预处理（LPL2020Spring_2022SpringData.py）和数据分析与挖掘（DataAnalytics.ipynb）。

## 🐠文件结构

- 🐼LPL2020Spring_2022SpringData.py: 包含了数据的采集、预处理和存储部分的代码。

- 🐨DataAnalytics.ipynb: 包含了数据分析部分的代码。

- 🦝/data: 数据分析所需的原始数据文件。

- 🐻/docs: 项目文档报告、PPT。

## 🦈功能与实现

`LPL2020Spring_2022SpringData.py`

    - 🐅数据采集部分：使用requests库和Selenium模拟浏览器访问数据API接口，获取数据，并使用BeautifulSoup解析网页数据。

    - 🐆数据预处理部分：将获取到的数据进行清洗和处理，包括数据选择、数据转换、数据排序等操作，并将处理后的数据写入到MySQL数据库中。

    - 🦨数据库连接和关闭：使用pymysql库连接本地MySQL数据库，进行数据的读写操作，并在数据处理完成后关闭数据库连接。

`DataAnalytics.ipynb`

    - 🦏数据读取部分：使用pandas库读取Excel文件中的数据，并进行数据检查。

    - 🐘多元线性回归模型拟合：使用最小二乘法（OLS）拟合多元线性回归模型，得到回归系数。

    - 🦍模型检验部分：对拟合的模型进行可决系数、标准估计误差和T检验等统计分析，评估模型的拟合效果和显著性。

## 🐳数据文件说明

    - 🦢/data: 包含了LPL2020-2022各战队的数据，用于数据分析部分的模型拟合和检验。
    - 🦚/docs: 包含了项目文档报告、PPT。

## 🐋使用说明
    🙈1.在确保安装了所需的Python库的前提下，分别运行LPL2020Spring_2022SpringData.py和DataAnalytics.ipynb文件。

    🙊2.执行LPL2020Spring_2022SpringData.py文件将完成数据的采集、预处理和存储。
    
    🙉3.执行DataAnalytics.ipynb文件将完成数据的读取、多元线性回归模型的拟合与检验。
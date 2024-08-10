import requests
import json
import time
import pandas as pd
import pprint
import pymysql
from tqdm import tqdm

from Crypto.Cipher import AES  # AES加密
from Crypto.Util.Padding import unpad  # 去填充
import base64  # base64解码


url = "https://app.swguancha.com/client/v1/cPublic/consumer/baseInfo"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,ko;q=0.4,fr;q=0.3",
    "Connection": "keep-alive",
    "Content-Length": "173",
    "Content-Type": "application/json;charset=UTF-8",
    "Devicetype": "1",
    "Host": "app.swguancha.com",
    "Origin": "https://www.swguancha.com",
    "Referer": "https://www.swguancha.com/",
    "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}

for i in tqdm(range(0, 53), colour='green', desc="城市数据获取"):
    data = {
        "size": 6,
        "current": "{}".format(i+1),
        "propertyCode": [
            "DISTRICT_PROP_GJ025_RJDQSCZZ",
            "DISTRICT_PROP_GJ117_NMSYGGQDCYYCLS",
            "DISTRICT_PROP_GJ001_NMHJRK"
        ],
        "dimensionTime": "2019",
        "levelType": 2
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    # print(resp.text)  # 返回的是加密的数据，格式为base64

    # js代码传输数据的逻辑
    """
    if ("string" === typeof t.data && t.data.length > 0)
        if ("{" === t.data[0]) {
            var e = JSON.parse(t.data);
            t.data = e
        } else {
            var n = u.enc.Utf8.parse(l)  # t.data是加密的 l是密钥 u.enc.Utf8.parse将密钥转换成utf-8格式 密钥是固定的"QV1f3nHn2qm7i3xrj3Y9K9imDdGTjTu9"
              , r = u.AES.decrypt(t.data, n, {  # AES解密  pip install pycryptodome
                mode: u.mode.ECB,  # 模式ECB
                padding: u.pad.Pkcs7  # 填充pkcs7
            })
              , i = r.toString(u.enc.Utf8)
              , s = JSON.parse(i);
            t.data = s
        }
    """

    # 从浏览器控制台中提取key和mode
    key = "QV1f3nHn2qm7i3xrj3Y9K9imDdGTjTu9"
    mode = AES.MODE_ECB

    # AES解密
    aes = AES.new(key=key.encode("utf-8"), mode=mode)
    ming = unpad(aes.decrypt(base64.b64decode(resp.text)), 16).decode("utf-8")  # AES处理的数据必须是16的倍数，所以要去填充。unpad完成后，返回的是bytes类型，换成str类型（utf-8编码）
    data = json.loads(ming)['data']['data']
    # pprint.pprint(data)

    cityCode_list = []
    cityName_list = []
    viewCount_list = []
    cityKpiNum_list = []
    dimensionTime_list = []
    popularValue_list = []
    gdpValue_list = []
    busValue_list = []

    for j in range(len(data)):
        cityCode = data[j]['cityCode']  # 城市编码
        cityName = data[j]['cityName']  # 城市名称
        viewCount = data[j]['viewCount']  # 浏览量
        cityKpiNum = data[j]['cityKpiNum']  # 城市指标数量
        simpleVOList = data[j]['simpleVOList']  # 数据列表
        # pprint.pprint(simpleVOList)
        for k in range(len(simpleVOList)):
            popularValue = None
            gdpValue = None
            busValue = None
            dimensionTime = simpleVOList[0]['dimensionTime']  # 维度时间
            try:
                if simpleVOList[0]['valueUnit'] == "万人":
                    popularValue = simpleVOList[0]['propertyValue'] + simpleVOList[0]['valueUnit']  # 户籍人口（单位：万人）
                    if simpleVOList[1]['valueUnit'] == "元":
                        gdpValue = simpleVOList[1]['propertyValue'] + simpleVOList[1]['valueUnit']  # 人均GDP（单位：元）
                        busValue = simpleVOList[2]['propertyValue'] + simpleVOList[2]['valueUnit']  # 公交车数量（单位：辆）
                    else:
                        gdpValue = simpleVOList[2]['propertyValue'] + simpleVOList[1]['valueUnit']
                        busValue = simpleVOList[1]['propertyValue'] + simpleVOList[2]['valueUnit']
                elif simpleVOList[0]['valueUnit'] == "元":
                    gdpValue = simpleVOList[0]['propertyValue'] + simpleVOList[0]['valueUnit']
                    if simpleVOList[1]['valueUnit'] == "万人":
                        popularValue = simpleVOList[1]['propertyValue'] + simpleVOList[1]['valueUnit']
                        busValue = simpleVOList[2]['propertyValue'] + simpleVOList[2]['valueUnit']
                    else:
                        popularValue = simpleVOList[2]['propertyValue'] + simpleVOList[2]['valueUnit']
                        busValue = simpleVOList[1]['propertyValue'] + simpleVOList[1]['valueUnit']
                else:
                    busValue = simpleVOList[0]['propertyValue'] + simpleVOList[0]['valueUnit']
                    if simpleVOList[1]['valueUnit'] == "万人":
                        popularValue = simpleVOList[1]['propertyValue'] + simpleVOList[1]['valueUnit']
                        gdpValue = simpleVOList[2]['propertyValue'] + simpleVOList[2]['valueUnit']
                    else:
                        popularValue = simpleVOList[2]['propertyValue'] + simpleVOList[2]['valueUnit']
                        gdpValue = simpleVOList[1]['propertyValue'] + simpleVOList[1]['valueUnit']
            except:
                pass

            cityCode_list.append(cityCode)
            dimensionTime_list.append(dimensionTime)
            cityName_list.append(cityName)
            viewCount_list.append(viewCount)
            cityKpiNum_list.append(cityKpiNum)
            popularValue_list.append(popularValue)
            gdpValue_list.append(gdpValue)
            busValue_list.append(busValue)
        time.sleep(0.5)

    df = pd.DataFrame({"cityCode": cityCode_list, "dimensionTime": dimensionTime_list, "cityName": cityName_list, "viewCount": viewCount_list,
                       "cityKpiNum": cityKpiNum_list, "popularValue": popularValue_list, "gdpValue": gdpValue_list, "busValue": busValue_list})
    df.drop_duplicates(subset="cityCode", inplace=True)  # 去重

    # 连接到 MySQL 服务器
    connection = pymysql.connect(
        host='localhost',  # MySQL 服务器地址
        user='root',  # 用户名
        password='ShadowZed666',  # 密码
    )
    # 创建一个游标对象
    cursor = connection.cursor()

    # 创建数据库
    databaseName = '数位观察'
    tableName = 'city'
    createDatabase = f"CREATE DATABASE IF NOT EXISTS {databaseName}"
    cursor.execute(createDatabase)

    # 使用创建的数据库
    cursor.execute(f"USE {databaseName}")

    # 创建表
    createTable = f"""
                    CREATE TABLE IF NOT EXISTS {tableName}
                    (cityCode INT,
                    dimensionTime INT,
                    cityName VARCHAR(255),
                    viewCount INT,
                    cityKpiNum INT,
                    popularValue VARCHAR(255),
                    gdpValue VARCHAR(255),
                    busValue VARCHAR(255));
                    """
    cursor.execute(createTable)
    # 存储数据至MySQL
    insert_query = f"""INSERT INTO {tableName} (cityCode, dimensionTime, cityName, viewCount, cityKpiNum, popularValue, gdpValue, busValue)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(insert_query, df.values.tolist())
    connection.commit()
    cursor.close()
    connection.close()

print("数据获取完毕，已存储至MySQL数据库")
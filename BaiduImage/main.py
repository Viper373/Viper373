import requests
import re
import time
import os


def saveImg(imgurlList, imgOs):
    for i in imgurlList:
        try:
            response = requests.get(url=i).content
        except:
            print("error!")
        else:
            imgName = i[28: 36]
            with open(imgOs + imgName + ".jpg", "wb") as file:
                file.write(response)
            print(i + " 下载完成！!")


def get_asjson(page, gsm, word):
    url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=9123806616981181340&ipn=rj&ct=201326592&is=&fp=result&fr=&word={word}&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={str(30 * int(page))}&rn=30&gsm={gsm}&{str(int(time.time() * 1000))}="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1637758492843_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDYsMiw0LDEsNSw4LDcsOQ%3D%3D&ie=utf-8&sid=&word=hello',
        'Cookie': 'BDqhfp=hello%26%26-10-1undefined%26%2628989%26%2635; BAIDUID=0C2336F5F3D356371C46DF079632E0C8:FG=1; BAIDUID_BFESS=0C2336F5F3D356371C46DF079632E0C8:FG=1; BIDUPSID=0C2336F5F3D356371C46DF079632E0C8; __yjs_duid=1_32693704d239fea9266064fc8a3d25631637737833661; PSTM=1637737880; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; delPer=0; PSINO=6; __yjs_st=2_ZGU4ODA5ZTdmNzczMzgxNzRiZWZhNTdkODVkY2E5MzQ3NzM3Nzc2MzZlNjYzZmRiMWVjOTlmNWQzZDA3NWY1MzM2M2NkNjNmMjMzZWVlYzQxNGQ2ODIzYjlkNTdhYTUyZjdhNWQwNjQxZWE1YTI0MWZiNzQ1NTE0N2NlNTgwNjZjODlkNWVlZWI2ZDBkNjUzNmNiZDE3NzUyYTA4ZjkxYjI1NzNhODBjOGZhZTBmMzZkY2IwOWJmNjMxNjEzNmUxYjQxZmZhM2M1ODUzYTFkNTM4NTE5MzZjZjRkODliMTE1MmRmMDY1MjI4OGJiM2I3ZGMzMDdiNjI4MWE3NDgxZV83XzQyODU3N2M0; H_PS_PSSID=35295_34446_35104_31254_35237_35049_34584_34505_35245_34578_34872_26350_35210_35145_22160; indexPageSugList=%5B%22hello%22%2C%22bello%22%2C%22hello%20%22%5D; cleanHistoryStatus=0; ab_sr=1.0.1_MTJmNTIwNGNlNmI5NDg2YmZiZTI1OTM1MGZhNTJhZTZlMzVmODE2NmEwZjg5MjNlZWZjZWY1YTY3ZjQ2Yzc2MWZiNGRlODY2ZDJjOGE3N2RhMzg2NjcxZjEzY2ZiMDQ4ODNjYzgyZTZlNWM2NGQ4YjlhMzBlMWE1ZjU0ZTY2NzAxYmM0ZGRkOTM0MGI3NzUwOWZjODY2ODE5NmU1N2E1Yw=='
    }
    response = requests.get(url=url, headers=headers).text + "1111"
    gsm = re.findall('"gsm":"(.*?)",', response)[0]
    data = re.findall('"hoverURL":"(.*?)",', response)
    return gsm, data


if __name__ == "__main__":
    a = "1e"
    key_word = "在家医"  # 修改你要爬取的关键字
    img = key_word + "_img\\"
    os.mkdir(img)
    for i in range(1, 2):  # 通过改变第二个数，修改要爬取的页数
        asjson1 = get_asjson(i, a, key_word)
        saveImg(asjson1[1], img)
        a = asjson1[0]
        while True:
            asjson2 = get_asjson(int(i) + 1, a, key_word)
            saveImg(asjson2[1], img)
            a = asjson2[0]
            break
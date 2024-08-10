import re
import requests


class SmsForwarder:
    def __init__(self):
        self.url = "https://api.sl.willanddo.com/api/msg/getMsgList?lastId=0"
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,ko;q=0.4,fr;q=0.3",
            "Connection": "keep-alive",
            "Host": "api.sl.willanddo.com",
            "Origin": "https://msg.allmything.com",
            "Referer": "https://msg.allmything.com/",
            "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Token": "3704f0ac27b38ac53e6a8985b06975b7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        }

    def forward(self):
        response = requests.get(url=self.url, headers=self.headers)
        return re.search(r"验证码：(\d{6})", response.json().get('result')[-1].get('content')).group(1)

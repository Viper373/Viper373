import requests
import json
from wxauto import WeChat


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=rDgyqHyNyOi7ixxITxvuavAo&client_secret=oRxnZrsI7FdjIWxLoilRvdVzRsiTSg9Q"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def main(wx, msg):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": msg
            },
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_result = json.loads(response.text)
    wx.SendMsg(msg=json_result['result'], who="盾宝🐰（玉桂狗版")

    print(response.text)


if __name__ == '__main__':
    wx = WeChat()
    while True:
        msgs = wx.GetAllMessage()

        if msgs:
            if msgs[-1].type == 'friend':
                main(wx, msgs[-1].content)

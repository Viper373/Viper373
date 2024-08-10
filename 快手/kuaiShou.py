import requests
import re

from tqdm import tqdm

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,ko;q=0.4,fr;q=0.3",
    "Connection": "keep-alive",
    "Content-Length": "1813",
    "Content-Type": "application/json",
    "Cookie": "did=web_60c41b70f4d148f199719f5c32df4277; didv=1710860626000; kpf=PC_WEB; clientid=3; userId=936150664; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABehMeb89o8QyuaAM17nggHbOOpvHOzn1ZSPYUKPqlRnbShbEmVw_xpeQ-gdqNCOJk4SrfEhHr06GhKX-uIknOOIdzKmmF0h7B9il9D3n6Hgf6QZs4GkdRh3c17jJVJBBmSNNe4pBm3m7MYB39KuTceEIXCE3lz4ZM2Nopnr13pRgPrBa036MZXjIpFONGfqoZg3PS8DdHl_a658rP7ui7IxoSnIqSq99L0mk4jolsseGdcwiNIiCi2Xao_uXI6PoEkw3WQdAVwWrcgIifR5k0ulbeMI8k3SgFMAE; kuaishou.server.web_ph=f966e193a66161c51cac0ef5fdafc2ada4c0; kpn=KUAISHOU_VISION",
    "Host": "www.kuaishou.com",
    "Origin": "https://www.kuaishou.com",
    "Referer": "https://www.kuaishou.com/short-video/3xsah7mxvhcthes?authorId=3xgz9zaku7hig96&streamSource=profile&area=profilexxnull",
    "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}
json = {"operationName": "visionProfilePhotoList",
         "variables": {"userId": "3xgz9zaku7hig96", "pcursor": "", "page": "detail", "webPageArea": "profilexxnull"},
         "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"
         }

json2 = {"operationName": "visionProfilePhotoList",
        "variables": {"userId": "3xgz9zaku7hig96", "pcursor": "1.697717370931E12", "page": "detail", "webPageArea": "profilexxnull"},
        "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}
url = "https://www.kuaishou.com/graphql"
response = requests.post(url=url, json=json, headers=headers)
json_data = response.json()
feeds = json_data['data']['visionProfilePhotoList']['feeds']
for feed in tqdm(feeds):
    caption = feed['photo']['caption']
    photoUrl = feed['photo']['photoUrl']
    re.sub(r'[\\/:*?<>|\n]', '', caption)
    video_data = requests.get(url=photoUrl).content
    with open(f'video/{caption}.mp4', mode='wb') as f:
        f.write(video_data)

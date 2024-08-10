import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def get_image_extension(url):
    """
    获取图片的扩展名
    """
    path = urlparse(url).path
    return os.path.splitext(path)[1].lower()


def download_images(url):
    """
    爬取指定URL中的所有图片（只包括JPG、PNG和JPEG），并保存到本地
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        allowed_extensions = ['.jpg', '.png', '.jpeg']

        for img_tag in img_tags:
            img_src = img_tag.get('src')
            if img_src:
                img_url = urljoin(url, img_src)
                img_extension = get_image_extension(img_url)

                if img_extension in allowed_extensions:
                    # 使用requests下载图片
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()

                    # 保存图片到本地
                    img_filename = os.path.basename(urlparse(img_url).path)
                    with open(img_filename, 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"已下载图片：{img_url}")
                else:
                    print(f"跳过图片（非JPG、PNG或JPEG）：{img_url}")

    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
    except Exception as ex:
        print(f"出现异常：{ex}")


if __name__ == "__main__":
    target_url = "https://www.corrain.top/"  # 替换为你要爬取图片的链接
    download_images(target_url)

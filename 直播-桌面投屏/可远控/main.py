# 可以操控屏幕

import pyautogui
from flask import Flask, render_template, Response, request
import win32api, win32con
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pointer')
def pointer():
    xpx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
    ypx = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
    x = int(float(request.args["xrate"]) * xpx)
    y = int(float(request.args["yrate"]) * ypx)
    # 执行点击操作
    pyautogui.click(x, y)
    return "success"


def gen():
    while True:
        screenShotImg = pyautogui.screenshot()

        imgByteArr = io.BytesIO()
        screenShotImg.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()
        frame = imgByteArr
        yield (b'--frame\r\n Content-Type: image/jpeg\r\n\r\n' + frame)


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True, threaded=True)

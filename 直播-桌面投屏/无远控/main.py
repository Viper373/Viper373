# 不可以操控屏幕

import io
import pyaudio
import pyautogui
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# ----------------- 视频传输 -----------------
@app.route('/video_feed')
def video_feed():
    def image():
        while True:
            screenShotImg = pyautogui.screenshot()
            screenShotImg = screenShotImg.resize((1920, 1080))  # 设置分辨率
            imgByteArr = io.BytesIO()
            screenShotImg.save(imgByteArr, format='JPEG')  # quality=40是图片压缩比率
            imgByteArr = imgByteArr.getvalue()
            frame = imgByteArr
            yield b'--frame\r\n Content-Type: image/jpeg\r\n\r\n' + frame

    return Response(image(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=60, host='0.0.0.0', debug=True, threaded=True)

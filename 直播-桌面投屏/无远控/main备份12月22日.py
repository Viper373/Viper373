# 不可以操控屏幕
import base64

import pyautogui
from pyaudio import PyAudio, paInt16
from flask import Flask, render_template, Response
import io
import pyaudio

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
            # screenShotImg = screenShotImg.resize((2560, 1440))  # 设置画质
            imgByteArr = io.BytesIO()
            screenShotImg.save(imgByteArr, format='JPEG')  # quality=40是图片压缩比率
            imgByteArr = imgByteArr.getvalue()
            frame = imgByteArr
            yield b'--frame\r\n Content-Type: image/jpeg\r\n\r\n' + frame

    return Response(image(), mimetype='multipart/x-mixed-replace; boundary=frame')


# ----------------- 音频传输 有电流音 -----------------
def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000 * 10 ** 6
    o = bytes("RIFF", 'ascii')  # (4byte) Marks file as RIFF 将文件标记为 RIFF
    o += (datasize + 36).to_bytes(4, 'little')  # (4byte) File size in bytes excluding this and RIFF marker 文件大小（以字节为单位），不包括此和 RIFF 标记
    o += bytes("WAVE", 'ascii')  # (4byte) File type 文件类型
    o += bytes("fmt ", 'ascii')  # (4byte) Format Chunk Marker 格式化区块标记
    o += (16).to_bytes(4, 'little')  # (4byte) Length of above format data 上述格式数据的长度
    o += (1).to_bytes(2, 'little')  # (2byte) Format type (1 - PCM) 格式类型 （1 - PCM）
    o += channels.to_bytes(2, 'little')  # (2byte)
    o += sampleRate.to_bytes(4, 'little')  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2, 'little')  # (2byte)
    o += bitsPerSample.to_bytes(2, 'little')  # (2byte)
    o += bytes("data", 'ascii')  # (4byte) Data Chunk Marker 数据块标记
    o += datasize.to_bytes(4, 'little')  # (4byte) Data size in bytes 数据大小（以字节为单位）
    return o


@app.route('/audio_feed')
def audio_feed():
    def sound():
        FORMAT = pyaudio.paInt16  # 采样位数
        CHANNELS = 2  # 两声道
        RATE = 44100  # 采样频率
        CHUNK = 1024  # 每个缓冲区的帧数
        audio = pyaudio.PyAudio()  # 实例化对象
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, input_device_index=1,
                            frames_per_buffer=CHUNK)  # input_device_index为录制设备的编号

        while True:
            data = wav_header + stream.read(CHUNK)  # data类型为bytes,格式是wav
            yield data
    return Response(sound(), mimetype="audio/x-wav")


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True, threaded=True)

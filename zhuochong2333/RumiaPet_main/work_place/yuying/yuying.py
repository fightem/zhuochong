import re
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import os
import logging
import speech_recognition as sr
import pyttsx3
import json
import requests
import time

class SpeechRecognitionService():
    def __init__(self):
        self.access_token = self.get_access_token()

    def get_token(self):
        logging.info('开始获取token...')
        baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
        grant_type = "client_credentials"
        client_id = "QkY2O9AAQO96Sy4A6STGAItS"
        client_secret = "zyF6LeOZCdA4SvflhS2kyIsW5GjfLxY0"
        url = f"{baidu_server}grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
        res = requests.post(url)
        token = json.loads(res.text)["access_token"]
        return token

    def wen_yuyin(self,filename, token):
        logging.info('开始识别语音文件...')
        with open(filename, "rb") as f:
            speech = base64.b64encode(f.read()).decode('utf-8')
        size = os.path.getsize(filename)
        headers = {'Content-Type': 'application/json'}
        url = "https://vop.baidu.com/server_api"
        data = {
            "format": "wav",
            "rate": "16000",
            "dev_pid": "1536",
            "speech": speech,
            "cuid": "TEDxPY",
            "len": size,
            "channel": 1,
            "token": token,
        }

        req = requests.post(url, json.dumps(data), headers)
        result = json.loads(req.text)
        if result["err_msg"] == "success.":
            ocr_text = str(result['result'][0])
            return ocr_text
        else:
            return False

    def process_audio(self):
        """
        通过麦克风录制语音并进行识别和处理
        """
        logging.basicConfig(level=logging.INFO)
        wav_num = 0

        r = sr.Recognizer()
        # 启用麦克风
        mic = sr.Microphone()
        logging.info('录音中...')
        with mic as source:
            # 降噪
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)  #时间限制
        with open(f"00{wav_num}.wav", "wb") as f:
            f.write(audio.get_wav_data(convert_rate=16000))
        logging.info('录音结束，识别中...')
        token = self.get_token()
        # target = audio_baidu(f"00{wav_num}.wav", token)
        data = self.wen_yuyin(f"00{wav_num}.wav", token)
        return data
    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=e1adkIbaxkTYFNdUOeACBRP6&client_secret=UIlHoGkGHisD7dY3PKZScN1Zy234U21Y"
        payload = json.dumps("")
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

    def speech_recognition(self):
        message = self.process_audio()
        return message



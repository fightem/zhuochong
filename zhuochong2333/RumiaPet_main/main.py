import base64
import os
import logging
import speech_recognition as sr
import pyttsx3
import json
import requests
import time

def get_token():
    logging.info('开始获取token...')
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    client_id = "QkY2O9AAQO96Sy4A6STGAItS"
    client_secret = "zyF6LeOZCdA4SvflhS2kyIsW5GjfLxY0"
    url = f"{baidu_server}grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    res = requests.post(url)
    token = json.loads(res.text)["access_token"]
    return token


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=e1adkIbaxkTYFNdUOeACBRP6&client_secret=UIlHoGkGHisD7dY3PKZScN1Zy234U21Y"
    payload = json.dumps("")
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def wen_yuyin(filename, token):
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


def wenxin(msg):
    headers = {'Content-Type': 'application/json'}
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(
        get_access_token())
    payload = json.dumps({"messages": [{"role": "user", "content": f'{msg}'}], "stream": True})
    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    list = []
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8").replace("data: ", ""))
            msg = data["result"]
            print(msg)
            yield msg
            # list.append(msg)
            # if len(list)>300:
            #     return list
            # engine = pyttsx3.init()
            # engine.say(msg)
            # engine.runAndWait()
    # return list


def process_audio():
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
        audio = r.listen(source)
    with open(f"00{wav_num}.wav", "wb") as f:
        f.write(audio.get_wav_data(convert_rate=16000))
    logging.info('录音结束，识别中...')
    token = get_token()
    # target = audio_baidu(f"00{wav_num}.wav", token)
    data = wen_yuyin(f"00{wav_num}.wav", token)
    return data




if __name__ == '__main__':
    data = process_audio()
    print(data)
    wenxin(data)
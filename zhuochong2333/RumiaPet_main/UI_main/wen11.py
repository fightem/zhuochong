my_input= "武汉理工大学怎么样"
import base64
import os
import logging
import speech_recognition as sr
import pyttsx3
import json
import requests
import time
from main import get_access_token

headers = {'Content-Type': 'application/json'}
url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(
    get_access_token())
# payload = json.dumps({"messages": [{"role": "user", "content": f'{my_input}'}]})
# response = requests.request("POST", url, headers=headers, data=payload)
#
payload = json.dumps({"messages": [{"role": "user", "content": f'{my_input}'}], "stream": True})
response = requests.request("POST", url, headers=headers, data=payload, stream=True)

list = []
count_len=0
for line in response.iter_lines():
    if line:
        data = json.loads(line.decode("utf-8").replace("data: ", ""))
        msg = data["result"]
        list.append(msg)
        count_len+=len(msg)
        if count_len>300:
            break
        # 这个是不流
        # engine = pyttsx3.init()
        # engine.say(msg)
        #
        # engine.runAndWait()
print(','.join(list))
 # 这个是流狮的传输，得到的为一段一段的输出
import requests
import random
import json
from hashlib import md5

def translate_text(query, from_lang='en', to_lang='zh'):
    # 设置你自己的 appid/appkey。
    appid = '20240222001970292'
    appkey = 'uCBTLM_IlM9hf916fA2r'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # 解析JSON数据，选择目标内容
    trans_result = result.get('trans_result', [])
    filtered_results = [item['dst'] for item in trans_result]

    return filtered_results

# 示例用法
query = ''
translated_text = translate_text(query, from_lang='zh', to_lang='en')

for text in translated_text:
    print(text)

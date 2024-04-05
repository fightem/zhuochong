import requests
import random
from hashlib import md5

class BaiduTranslator:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        self.endpoint = 'http://api.fanyi.baidu.com'
        self.path = '/api/trans/vip/translate'
        self.url = self.endpoint + self.path

    def translate_text(self, query, from_lang='en', to_lang='zh'):
        def make_md5(s, encoding='utf-8'):
            return md5(s.encode(encoding)).hexdigest()

        salt = random.randint(32768, 65536)
        sign = make_md5(self.appid + query + str(salt) + self.appkey)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        # 解析JSON数据，选择目标内容
        trans_result = result.get('trans_result', [])
        filtered_results = [item['dst'] for item in trans_result]

        return filtered_results

# 使用示例
translator = BaiduTranslator('20240222001970292', 'uCBTLM_IlM9hf916fA2r')
translation = translator.translate_text('Hello, how are you?')
print(translation)

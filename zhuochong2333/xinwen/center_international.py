from lxml import etree
import requests

# 定义常量
URL = "https://tophub.today/n/RrvWOl3v5z"  # 观察者网
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.69'
}
XPATH_TR = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr'

# 使用持久化连接
session = requests.Session()
res = session.get(url=URL, headers=HEADERS)
html = etree.HTML(res.text)

# 使用with管理文件操作
with open("guojixinwen.txt", mode="w", encoding="utf-8") as file:
    trs = html.xpath(XPATH_TR)
    for num, tr in enumerate(trs):
        if num == 15:
            break
        id = tr.xpath('./td[1]/text()')[0].split('.')[0]
        title = tr.xpath('./td[2]/a/text()')[0]
        href = tr.xpath('./td[2]/a/@href')[0]
        play = tr.xpath('./td[3]/text()')[0]

        msg = f"新闻{id} {title}"
        print(id, title, play, href)

        file.write(msg + "\n")

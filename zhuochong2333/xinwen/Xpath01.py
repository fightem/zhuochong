import requests
from lxml import etree

url = "https://m.guancha.cn/internation/2023_05_09_691589.shtml"
print(url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

t = requests.get(
    url=url,
    headers=headers
)
# sleep(1)

html = etree.HTML(t.text)
# print(html)
# print(etree.tostring(html, pretty_print=True).decode("utf-8"))  # 打印HTML内容
contents = html.xpath('*//div[@class="gc_content"]/p') #//div[@class="content all-txt"]/p

text = ''
for content in contents:
    # 确保content.text不为空
    if content.text:
        text += content.text.strip()  # 添加换行符以便于区分段落

print(text)



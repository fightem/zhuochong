from lxml import etree
import requests
import re

def get_news_list(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    res = requests.get(
        url=url,
        headers=headers
    )
    news_list = []

    html = etree.HTML(res.text)
    print(html)
    # trs=html.xpath('ml/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr')
    trs = html.xpath('//div[@class="video-card__info"]/p[1]')
    # hrefs = html.xpath('//div[@class="index_contentBox__070hn"]/a/@href')

    i = 0
    for tr in trs[0:15]:
        title = tr.xpath('string(.)').strip()
        # tr.xpath('string(.)')
        # 这一行代码是从tr对象中提取文本内容。string(.) 表示获取当前节点的文本内容。
        # .strip()
        # 是去除文本前后的空白字符, 使得获取到的标题更加干净。

        href = "https://www.bilibili.com/v/popular/weekly/?num=260"
        content = "此条新闻为视频内容，请点击上方 '阅读原文' 查看原视频"
        id = i + 1
        i += 1
        # print(id, title, href, content)
        news_list.append({'id': id, 'title': title, 'href': href, 'content': content})

    return news_list


if __name__ == "__main__":
    # Example usage:
    url = "https://www.bilibili.com/v/popular/weekly?num=260"  # 观察者网
    news_list = get_news_list(url)
    for news in news_list:
        print(news)
        print("*"*50)
        print("\n")

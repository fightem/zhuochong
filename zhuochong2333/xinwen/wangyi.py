from lxml import etree
import requests
import re


def get_content(href):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    url_zi = href
    print(url_zi)
    t = requests.get(
        url=url_zi,
        headers=headers
    )
    # sleep(1)

    html = etree.HTML(t.text)
    print(html)
    contents = html.xpath('//div[@class="article-body"]/div/p')

    text = ''
    # 确保content.text不为空
    for content in contents:
        if content.text:
            text += content.text.strip()  # 添加换行符以便于区分段落

    if text == '':
        text = "此条新闻为视频内容，请点击上方 '阅读原文' 查看原视频"

    return text


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
    # trs=html.xpath('ml/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr')
    trs = html.xpath('//td[2]')
    hrefs = html.xpath('//td[2]/a/@href')
    print(trs)

    i = 0
    for tr in trs[0:15]:
        title = tr.xpath('string(.)').strip()
        # tr.xpath('string(.)')
        # 这一行代码是从tr对象中提取文本内容。string(.) 表示获取当前节点的文本内容。
        # .strip()
        # 是去除文本前后的空白字符, 使得获取到的标题更加干净。

        href = hrefs[i]
        href = "https://tophub.today" + href
        content = get_content(href)
        id = i + 1
        i += 1
        # print(id, title, href, content)
        news_list.append({'id': id, 'title': title, 'href': href, 'content': content})

    return news_list


if __name__ == "__main__":
    # Example usage:
    url = "https://tophub.today/n/ENeYa4DeY4"  # 网易新闻
    news_list = get_news_list(url)
    for news in news_list:
        print(news)
        print("*" * 50)
        print("\n")

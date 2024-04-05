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
    contents = html.xpath('*//div[@class="gc_content"]/p')

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
    trs = html.xpath('//div[@class="newListR"]/a/*[1]')
    hrefs = html.xpath("//div[@class='newListR']/a/@href")
    print(trs)

    i = 0
    for tr in trs[0:15]:
        title = tr.xpath('string(.)').strip()
        # tr.xpath('string(.)')
        # 这一行代码是从tr对象中提取文本内容。string(.) 表示获取当前节点的文本内容。
        # .strip()
        # 是去除文本前后的空白字符, 使得获取到的标题更加干净。



        # # 使用正则表达式匹配并提取前面的文字
        # match = re.match(r'(.*?)\d+', title)
        # if match:
        #     clean_title = match.group(1).strip()
        #     title = clean_title

        href = hrefs[i]
        href = "https://m.guancha.cn" + href
        content = get_content(href)
        id = i + 1
        i += 1
        # print(id, title, href, content)
        news_list.append({'id': id, 'title': title, 'href': href, 'content': content})

    return news_list



# def get_news_list(url):
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.69'
#     }
#     res = requests.get(url=url, headers=headers)
#
#     html = etree.HTML(res.text)
#     trs = html.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr')
#
#     news_list = []
#
#     for tr in trs[0:15]:
#         id = tr.xpath('./td[1]/text()')[0]
#         title = tr.xpath('./td[2]/a/text()')[0]
#         href = tr.xpath('./td[2]/a/@href')[0]
#         href = "https://tophub.today"+href
#
#         request = requests.get(
#             url=href,
#             headers=headers
#         )
#         content = etree.HTML(request.text)
#         news_list.append({'id': id, 'title': title, 'href': href, 'content':content})
#
#     return news_list


if __name__ == "__main__":
    # Example usage:
    url = "https://m.guancha.cn/internation"  # 观察者网
    news_list = get_news_list(url)
    for news in news_list:
        print(news)
        print("*"*50)
        print("\n")

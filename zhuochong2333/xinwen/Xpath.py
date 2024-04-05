from lxml import etree
from selenium import webdriver
import requests
import re

def get_content(href):
    # 设置浏览器驱动路径
   executable_path = r'your_webdriver_executable_path\chromedriver.exe'
    # 创建 Chrome WebDriver 实例
    driver = webdriver.Chrome(executable_path)

    # 打开指定网页
    driver.get(href)

    # 等待页面加载完成
    # 可以根据需要调整等待时间
    driver.implicitly_wait(10)

    # 获取页面内容
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    # 使用 lxml.etree 解析 HTML
    html = etree.HTML(html)
    contents = html.xpath('//div[@class="article-body"]/div/p')

    text = ''
    # 确保 content.text 不为空
    for content in contents:
        if content.text:
            text += content.text.strip()  # 添加换行符以便于区分段落

    if text == '':
        text = "此条新闻为视频内容，请点击上方 '阅读原文' 查看原视频"

    return text

def get_news_list(url):
    # 设置浏览器驱动路径
    executable_path = r'your_webdriver_executable_path\chromedriver.exe'
    # 创建 Chrome WebDriver 实例
    driver = webdriver.Chrome(executable_path)

    # 打开指定网页
    driver.get(url)

    # 等待页面加载完成
    # 可以根据需要调整等待时间
    driver.implicitly_wait(10)

    # 获取页面 HTML 源代码
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    # 使用 lxml.etree 解析 HTML
    html = etree.HTML(html)
    # trs=html.xpath('ml/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr')
    trs = html.xpath('//td[2]')
    hrefs = html.xpath('//td[2]/a/@href')

    news_list = []

    i = 0
    for tr in trs[0:15]:
        title = tr.xpath('string(.)').strip()
        # tr.xpath('string(.)')
        # 这一行代码是从 tr 对象中提取文本内容。string(.) 表示获取当前节点的文本内容。
        #.strip()
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
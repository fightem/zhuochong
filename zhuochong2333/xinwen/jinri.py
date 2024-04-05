from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import requests

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
    contents = html.xpath('*//div[@class="index_cententWrap__Jv8jK"]/p')

    text = ''
    # 确保content.text不为空
    for content in contents:
        if content.text:
            text += content.text.strip()  # 添加换行符以便于区分段落

    if text == '':
        text = "此条新闻为视频内容，请点击上方 '阅读原文' 查看原视频"

    return text

def get_news_list(url):
    # 设置EdgeDriver选项
    options = Options()
    # 如果WebDriver文件与程序在同一文件夹下，可以使用相对路径
    driver_path = "./msedgedriver.exe"

    # 初始化Edge WebDriver
    service = Service(executable_path=driver_path)
    driver = webdriver.Edge(service=service, options=options)

    try:
        driver.get(url)

        # 等待网页加载
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "feed-card-article-l")))

        news_list = []

        html = etree.HTML(driver.page_source)
        trs = html.xpath('*//div[@class="feed-card-article-l"]/a[1]')
        hrefs = html.xpath('*//div[@class="feed-card-article-l"]/a/@href')
        i = 0
        for tr in trs[0:15]:
            title = tr.xpath('string(.)').strip()
            href = hrefs[i]
            content = get_content(href)
            id = i + 1
            i += 1
            news_list.append({'id': id, 'title': title, 'href': href, 'content': content})
    finally:
        driver.quit()

    return news_list

if __name__ == "__main__":
    # Example usage:
    url = "https://www.toutiao.com/"  # 今日头条
    news_list = get_news_list(url)
    for news in news_list:
        print(news)
        print("*"*50)
        print("\n")
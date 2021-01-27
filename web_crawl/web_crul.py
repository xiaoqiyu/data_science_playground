# -*- coding: utf-8 -*-
# @time      : 2019/5/6 10:52
# @author    : yuxiaoqi@cmschina.com.cn
# @file      : web_crul.py


import codecs
from urllib import request, parse
from bs4 import BeautifulSoup
import re
import time
from urllib.error import HTTPError, URLError
import sys

sys.setrecursionlimit(1000000)  # 设置递归次数为100万

# 伪装浏览器抬头以防和谐
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/51.0.2704.63 Safari/537.36'}


# 新闻类定义
class News(object):
    def __init__(self):
        self.url = None  # 该新闻对应的url
        self.topic = None  # 新闻标题
        self.date = None  # 新闻发布日期
        self.content = None  # 新闻的正文内容
        self.author = None  # 新闻作者


visited = set()  # 存储访问过的url
count = 0
fin = open('data/news1.txt', 'a+', encoding='utf-8')


# 如果url符合解析要求，则对该页面进行信息提取
def getNews(url):
    print('processing {0} in getNews'.format(url))
    # 获取页面所有元素
    html = request.urlopen(url).read().decode('gb2312', 'ignore')
    # 解析
    soup = BeautifulSoup(html, 'html.parser')
    # 获取信息
    if not (soup.find('div', {'id': 'leftnews'})):
        print('not found leftnews')
        # return
    news = News()  # 建立新闻对象
    # page = soup.find('div', {'id': 'leftnews'})
    # if not (page.find('div', {'class': 'newsConTit'})):
    #     print('return in newsConTit')
    #     return
    # topic = page.find('div', {'class': 'newsConTit'}).get_text()  # 新闻标题
    # news.topic = topic
    # print('get news topic:{0}'.format(news.topic))
    # if not (page.find('div', {'id': 'IDNewsDtail'})):
    #     print('return in IDNewDetail')
    #     return
    # main_content = page.find('div', {'id': 'IDNewsDtail'})  # 新闻正文内容
    # content = ''
    #
    # for p in main_content.select('p'):
    #     content = content + p.get_text()
    news.topic = soup.title.string
    content = soup.get_text()
    news.content = content

    news.url = url  # 新闻页面对应的url
    fin.write(news.topic + '\t' + news.content + '\n')


# dfs算法遍历全站
def dfs(url=None, count=0):
    print('start processing {0} in dfs'.format(url))

    # 下面的部分需要修改月份以更换爬取月份
    pattern1 = '^http://stock.jrj.com.cn/2015/06\/[a-z0-9_\/\.]*$'  # 可以继续访问的url规则
    pattern2 = '^http://stock.jrj.com.cn/2015/06\/[0-9]{14}\.shtml$'  # 解析新闻信息的url规则
    pattern3 = '^http://stock.jrj.com.cn/xwk/201001/201001[0-9][0-9]\_[0-9]\.shtml$'  # 测试

    # 该url访问过，则直接返回
    if url in visited:
        return
    # print(url)

    # 把该url添加进visited()
    visited.add(url)
    # print(visited)
    # 设置停顿时间为1秒
    time.sleep(2)
    try:
        # 该url没有访问过的话，则继续解析操作
        html = request.urlopen(url).read().decode('utf-8', 'ignore')
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')

        if re.match(pattern2, url):
            getNews(url)
        count += 1

        # 提取该页面其中所有的url
        links = soup.findAll('a', href=re.compile(pattern1))
        for link in links:
            print(link['href'])
            if link['href'] not in visited:
                dfs(link['href'], count)
            # count += 1
    except URLError as e:
        print(e)
        return
    except HTTPError as e:
        print(e)
        return
    print(count)
    if count > 3:
        return


def quick_test():
    # 获取页面所有元素
    html = request.urlopen('http://stock.jrj.com.cn/2019/05/10193427555277.shtml').read().decode('gb2312', 'ignore')
    # 解析
    soup = BeautifulSoup(html, 'html.parser')
    soup.head
    # get contents
    soup.find_all('div', attrs={'class': 'texttit_m1'})[0].get_text('|', strip=True).split('|')
    soup.head.title.string


if __name__ == '__main__':
    quick_test()

    # # 利用list对整个月份中所有的分页的进行遍历，此操作能够使得爬虫在遍历当前页面所有url的基础上，再遍历每个月份的所有分页内的所有新闻。
    # urls = ['http://stock.jrj.com.cn/xwk/201506/201506{}{}_{}.shtml'.format(str(i), str(j), str(k)) for i in range(0, 4) for
    #         j in range(1, 10) for k in range(1, 6)]
    # count = 0
    # for url in urls:
    #     if url == 'http://stock.jrj.com.cn/xwk/201905/20190510_5.shtml':  # 需要修改以更换月份
    #         dfs(url, count)
    #         break
    #     dfs(url, count)
    # else:
    #     dfs(url, count)
    # dfs(url, count)

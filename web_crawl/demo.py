# -*- coding: utf-8 -*-
# @time      : 2019/5/6 10:52
# @author    : yuxiaoqi@cmschina.com.cn
# @file      : web_crul.py

# https://blog.csdn.net/duxu24/article/details/77414298

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

g_count = 0
date = '2019-05-10'
#
#
# # 新闻类定义
# class News(object):
#     def __init__(self):
#         self.url = None  # 该新闻对应的url
#         self.topic = None  # 新闻标题
#         self.date = None  # 新闻发布日期
#         self.content = None  # 新闻的正文内容
#         self.author = None  # 新闻作者


visited = set()  # 存储访问过的url
count = 0
fin = open('data/news_jrj3.txt', 'a+', encoding='utf-8')


def get_news(url):
    print('processing {0} in getNews'.format(url))
    html = request.urlopen(url).read().decode('gb2312', 'ignore')

    # 解析
    soup = BeautifulSoup(html, 'html.parser')
    title, contents = '', ''
    try:
        # 获取信息
        # title = soup.head.title.string
        title = soup.title.get_text(strip=True)
        # get contents
        contents = soup.find_all('div', attrs={'class': 'texttit_m1'})[0].get_text('|', strip=True)
        text_div = soup.find('div', attrs={'class': 'texttit_m1'}).find_all('p')
        contents = ';'.join([item.get_text(strip=True) for item in text_div])
    except Exception as ex:
        print('fail to get the contents for url: {0} with error:{1}'.format(url, ex))
        return title, contents
    return title, contents


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
    # news = News()  # 建立新闻对象
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

    # news.topic = soup.title.string
    # content = soup.get_text()
    # news.content = content
    #
    # news.url = url  # 新闻页面对应的url
    # fin.write(news.topic + '\t' + news.content + '\n')


# dfs算法遍历全站
def dfs(url=None, date=''):
    global count
    global visited
    print('start processing {0} in dfs'.format(url))
    yy, mm, dd = date.split('-')
    # 下面的部分需要修改月份以更换爬取月份
    pattern1 = '^http://stock.jrj.com.cn/{0}/{1}\/[a-z0-9_\/\.]*$'.format(yy, mm)  # 可以继续访问的url规则
    pattern2 = '^http://stock.jrj.com.cn/2019/05\/[0-9]{14}\.shtml$'  # 解析新闻信息的url规则
    pattern3 = '^http://stock.jrj.com.cn/xwk/201001/201001[0-9][0-9]\_[0-9]\.shtml$'  # 测试

    # 该url访问过，则直接返回
    if url in visited:
        return

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
            # getNews(url)
            title, contents = get_news(url)
            fin.write(url + '\t' + title + '\t' + contents + '\n')
        count += 1
        # 提取该页面其中所有的url
        links = soup.findAll('a', href=re.compile(pattern1))
        for link in links:
            print(link['href'])
            if link['href'] not in visited:
                dfs(link['href'], date)
            # count += 1
    except URLError as e:
        print(e)
        return
    except HTTPError as e:
        print(e)
        return
    if count > 3:
        return


def quick_test():
    import urllib.request
    headers = {
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
               'Accept': r'application/json, text/javascript, */*; q=0.01',
              }
    req = urllib.request.Request(r'http://stock.jrj.com.cn/hotstock/2019/05/10140727553855.shtml', headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('gb2312', 'ignore')

    # 获取页面所有元素
    #带hearder的request
    req = urllib.request.Request(r'http://stock.jrj.com.cn/2019/05/10140427553851.shtml', headers=headers)
    response = urllib.request.urlopen(req)
    #直接url请求
    # response = request.urlopen('http://stock.jrj.com.cn/hotstock/2019/05/10140727553855.shtml')
    # html = response.read().decode('gb2312', 'ignore')

    # 解析
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.head)
    soup.find_all('div', attrs={'class': 'texttit_m1'})
    # get contents
    # soup.find_all('div', attrs={'class': 'texttit_m1'})[0].get_text('|', strip=True).split('|')
    print(soup.head.title.string)


def cookie_example():
    import http.cookiejar, urllib.request
    #获取cookie
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print(item.name+"="+item.value)

    #保存cookie(MozillaCookieJar)
    filename = 'data/cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    cookie.save(ignore_discard=True, ignore_expires=True)

    #使用cookie
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('data/cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))


def utllib_example():
    import urllib.request
    headers = {'Host': 'www.xicidaili.com',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
               'Accept': r'application/json, text/javascript, */*; q=0.01',
               'Referer': r'http://www.xicidaili.com/', }
    req = urllib.request.Request(r'http://www.xicidaili.com/nn/', headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    print(html)

def main(date='2019-05-10', page_num=5):
    yy, mm, dd = date.split('-')
    urls = ['http://stock.jrj.com.cn/xwk/{0}{1}/{2}{3}{4}_{5}.shtml'.format(yy, mm, yy, mm, dd, item) for item in
            range(1, page_num)]
    for url in urls:
        dfs(url, date)


if __name__ == '__main__':
    # cookie_example()
    # utllib_example()
    # main()
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

#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: crawl_example.py
@time: 19-5-16 下午8:05
@desc:
'''

import codecs
from urllib import request
from bs4 import BeautifulSoup
import re
import time
from urllib.error import HTTPError, URLError
import sys

sys.setrecursionlimit(1000000)  # 设置递归次数为100万

# 伪装浏览器抬头以防和谐
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/51.0.2704.63 Safari/537.36'}

date = '2019-05-10'
visited = set()  # 存储访问过的url
count = 0
#新闻数据存储的文件
fin = open('data/news_jrj1.txt', 'a+', encoding='utf-8')


def get_news(url):
    print("读取网页 {0} in get_news".format(url))
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


# dfs算法遍历全站
def dfs(url=None, date=''):
    global count
    global visited
    print("开始访问网页 {0}".format(url))
    yy, mm, dd = date.split('-')
    # 下面的部分需要修改月份以更换爬取月份
    pattern1 = '^http://stock.jrj.com.cn/{0}/{1}\/[a-z0-9_\/\.]*$'.format(yy, mm)  # 可以继续访问的url规则
    # pattern1 = '^http://stock.jrj.com.cn/xwk/{0}{1}\/[a-z0-9_\/\.]*$'.format(yy, mm)
    pattern2 = '^http://stock.jrj.com.cn/2019/05\/[0-9]{14}\.shtml$'  # 解析新闻信息的url规则

    # 该url访问过，则直接返回
    if url in visited:
        return

    # 把该url添加进visited()
    visited.add(url)
    # 设置停顿时间为1秒
    time.sleep(2)
    try:
        # 该url没有访问过的话，则继续解析操作
        #发送请求
        req = request.Request(url, headers=headers)
        html = request.urlopen(req)
        # html = request.urlopen(url).read().decode('utf-8', 'ignore')
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        #如果满足继续解析的url pattern，就获取网页内容，并写进文件
        if re.match(pattern2, url):
            title, contents = get_news(url)
            #将结果写入文件，每条记录存储格式为 “URL 标题  内容”
            fin.write(url + '\t' + title + '\t' + contents + '\n')
        count += 1
        # 提取该页面其中所有的url，递归遍历访问
        links = soup.findAll('a', href=re.compile(pattern2))
        for link in links:
            try:
                print(link['href'])
                if link['href'] not in visited:
                    # if re.findall(re.compile(pattern2), link['href']):
                    dfs(link['href'], date)
                 # count += 1
            except Exception as ex:
                pass
    except URLError as e:
        print(e)
        return
    except HTTPError as e:
        print(e)
        return


def cookie_example():
    import http.cookiejar, urllib.request
    #获取cookie
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print(item.name + "=" + item.value)

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


def set_header_example():
    headers = {'Host': 'www.xicidaili.com',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
               'Accept': r'application/json, text/javascript, */*; q=0.01',
               'Referer': r'http://www.xicidaili.com/', }
    req = request.Request(r'http://www.xicidaili.com/nn/', headers=headers)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    print(html)


def jrj_crawl(date='2019-05-10', page_num=5):
    yy, mm, dd = date.split('-')
    urls = ['http://stock.jrj.com.cn/xwk/{0}{1}/{2}{3}{4}_{5}.shtml'.format(yy, mm, yy, mm, dd, item) for item in
            range(1, page_num)]
    for url in urls:
        dfs(url, date)


if __name__ == '__main__':
    #获取和使用cookie例子
    # cookie_example()
    #url请求设置header例子
    #set_header_example()
    #JRJ爬虫例子入口
    jrj_crawl(date='2019-05-10', page_num=5)

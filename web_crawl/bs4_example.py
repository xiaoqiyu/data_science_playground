# -*- coding: utf-8 -*-
# @time      : 2019/5/13 13:19
# @author    : yuxiaoqi@cmschina.com.cn
# @file      : bs4_example.py

from bs4 import BeautifulSoup

# pip install lxml
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/    bs documents

# html源码例子
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# f = open('three_sister.html','rb')
# html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
# 读取标题文字
title = soup.head.title.string
print(title)
# 格式化打印
ret = soup.prettify()
# 找到所有链接的结点，返回列表对象
ret = soup.find_all('a')
ret = [item for item in soup.stripped_strings]
# 找到所有链接点中，id为'link3'的结点
soup.find('a', attrs={'id': 'link3'})
soup('a')  # 和 soup.find_all('a')一样
# 返回所有的text,并使用'|'符号间隔
soup.get_text('|').split('|')
soup.get_text('|', strip=True).split('|')

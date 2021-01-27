#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: text_mining.py
@time: 19-5-15 下午5:57
@desc:
'''

import os
import jieba
from jieba import analyse
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


def remove_stop_words(corpus=[]):
    file_path = 'data/stop_words.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read()
        words = list(set(corpus) - set(lines))
        return words
    return corpus


def corpus2words(corpus=None):
    if isinstance(corpus, list):
        if len(corpus) == 1:
            corpus = corpus[0]
        else:
            corpus = ','.join(corpus)
    corpus.encode(encoding='utf-8')
    ret = jieba.lcut(corpus, cut_all=False, HMM=False)
    return remove_stop_words(ret)


def _read_corpus():
    '''
    读取JRJ爬虫中获取的语料，新闻数据
    '''
    with open('data/news_jrj1.txt', encoding='utf-8') as fin:
        lines = fin.readlines()
        titles = [item.split('\t')[1] for item in lines]
        contents = [item.split('\t')[2] for item in lines]
    return titles, contents


def get_topics(corpus=None, topk=20):
    if isinstance(corpus, list):
        corpus = ','.join(corpus)
    # stop_word_dir_path = os.path.dirname(os.path.dirname(__file__))
    # stop_word_path = os.path.join(os.path.join(os.path.join(stop_word_dir_path, 'data'), 'material'), 'stop_words.txt')
    analyse.set_stop_words('data/stop_words.txt')
    # 获取排名前topK的词列表
    # tf-idf
    # pagerank

    ret = analyse.textrank(corpus, topK=topk, withWeight=True)
    print(ret)
    top_words = [str(item[0]) for item in ret]
    wc = WordCloud(background_color="white", max_font_size=120, random_state=42,
                   font_path="c:\windows\fonts\simsun.ttc")
    wc.generate(','.join(top_words))
    plt.imshow(wc)
    plt.show()


if __name__ == '__main__':
    titles, contents = _read_corpus()
    lst_of_words = corpus2words(contents[1])
    print(lst_of_words)
    topics = get_topics(contents, 10)

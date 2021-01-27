# -*- coding: utf-8 -*-
# @time      : 2019/5/6 11:11
# @author    : yuxiaoqi@cmschina.com.cn
# @file      : ocr_example.py

#baidu_acc: Ambitionltime
#pwd: *36**yu
#ref:https://ai.baidu.com/

import pprint
import re
from aip import AipOcr
import matplotlib.pyplot as plt

#以下三个变量更改为自己创建的对应的应用的ID和KEY
APP_ID = '16180738'
API_KEY = 'MFfasFCDE9nPfsca7hyPRRwG'
SECRET_KEY = 'k6t6hqeFOIyNK81RdqkmXiwaSBIOzQhW'

aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_fig_results(filePath = "test02.png"):
    # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

    #调用通用文字识别接口识别网上图片
    # url = ''
    # aipOcr.basicGeneralUrl(url, options)

    # 调用通用文字识别接口识别本地图片
    ret = aipOcr.basicAccurate(get_file_content(filePath), options)
    print("OCR接口返回结果")
    print(ret)
    data = ret.get('words_result')
    words = []
    plot_data = []
    #正则化匹配模式 '1,2,3,4,5'
    pattern = re.compile('\d,\d,\d,\d,\d')
    for item in data:
        words.append(item.get('words'))
    for idx, item in enumerate(words):
        #找到匹配上述模式的元素的下标
        if re.match(pattern, item):
            plot_data.append(words[idx-6: idx])
    #去掉百分号转换成数值类型
    cols = [float(item[2].strip('%')) for item in plot_data]
    plt.rcParams['font.sans-serif'] =['SimHei']
    plt.plot(cols)
    plt.title(u"组合1年化超额收益率")
    plt.ylabel(u"收益率%")
    plt.xlabel(u"行业")
    plt.show()
    return plot_data


if __name__ == '__main__':
    ret = get_fig_results('data/test02.png')
    pprint.pprint(ret)

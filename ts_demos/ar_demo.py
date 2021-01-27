#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: ar_demo.py
@time: 2021/1/18 16:57
@desc:
'''

import pprint
import numpy as np
import pandas as pd
import uqer
import os
from uqer import DataAPI
import matplotlib.pyplot as plt
from utils.io_utils import load_json_file
from utils.logger import Logger
from scipy import stats
import statsmodels.api as sm

logger = Logger().get_log()


def initialize():
    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(PROJECT_ROOT, "..\\conf\\accounts.json")
    acc_conf = load_json_file(path)
    try:
        uqer_client = uqer.Client(token=acc_conf.get('uqer')[1])
    except Exception as ex:
        logger.error("Uqer Login exception with error:{0}".format(ex))


def ts_analysis():
    IndexData = DataAPI.MktIdxdGet(indexID=u"", ticker=u"000001", beginDate=u"20150101", endDate=u"20201231",
                                   field=u"tradeDate,closeIndex,CHGPct", pandas="1")
    IndexData = IndexData.set_index(IndexData['tradeDate'])

    IndexData['colseIndexDiff_1'] = IndexData['closeIndex'].diff(1)  # 1阶差分处理
    IndexData['closeIndexDiff_2'] = IndexData['colseIndexDiff_1'].diff(1)  # 2阶差分处理

    # plot
    # print(IndexData.columns)
    # IndexData.plot(subplots=True, figsize=(18, 12))
    # plt.show()

    # ts analysis of the close
    data = IndexData['closeIndex']  # 上证指数
    m = 10  # 我们检验10个自相关系数

    acf, q, p = sm.tsa.acf(data, nlags=m, qstat=True)  ## 计算自相关系数 及p-value
    out = np.c_[range(1, 11), acf[1:], q, p]
    output = pd.DataFrame(out, columns=['lag', "AC", "Q", "P-value"])
    output = output.set_index('lag')
    pprint.pprint(output)

    # ts analysis of  the return
    data2 = IndexData['CHGPct']  # 上证指数日涨跌
    m = 10  # 我们检验10个自相关系数

    acf, q, p = sm.tsa.acf(data2, nlags=m, qstat=True)  ## 计算自相关系数 及p-value
    out = np.c_[range(1, 11), acf[1:], q, p]
    output = pd.DataFrame(out, columns=['lag', "AC", "Q", "P-value"])
    output = output.set_index('lag')

    # ar model example
    temp = np.array(data2)  # 载入收益率序列
    model = sm.tsa.AR(temp)
    results_AR = model.fit()
    plt.figure(figsize=(10, 4))
    plt.plot(temp, 'b', label='CHGPct')
    plt.plot(results_AR.fittedvalues, 'r', label='AR model')
    plt.legend()

    print(len(results_AR.roots))

    # 画出特征根
    pi, sin, cos = np.pi, np.sin, np.cos
    r1 = 1
    theta = np.linspace(0, 2 * pi, 360)
    x1 = r1 * cos(theta)
    y1 = r1 * sin(theta)
    plt.figure(figsize=(6, 6))
    plt.plot(x1, y1, 'k')  # 画单位圆
    roots = 1 / results_AR.roots  # 注意，这里results_AR.roots 是计算的特征方程的解，特征根应该取倒数
    for i in range(len(roots)):
        plt.plot(roots[i].real, roots[i].imag, '.r', markersize=8)  # 画特征根
    plt.show()

    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(111)
    fig = sm.graphics.tsa.plot_pacf(temp, ax=ax1)
    # plt.show()

    # AIC, BIC,HQ信息准则筛选模型
    aicList = []
    bicList = []
    hqicList = []
    for i in range(1, 11):  # 从1阶开始算
        order = (i, 0)  # 这里使用了ARMA模型，order 代表了模型的(p,q)值，我们令q始终为0，就只考虑了AR情况。
        tempModel = sm.tsa.ARMA(temp, order).fit()
        aicList.append(tempModel.aic)
        bicList.append(tempModel.bic)
        hqicList.append(tempModel.hqic)

    plt.figure(figsize=(15, 6))
    plt.plot(aicList, 'r', label='aic value')
    plt.plot(bicList, 'b', label='bic value')
    plt.plot(hqicList, 'k', label='hqic value')
    plt.legend(loc=0)
    plt.show()

    # 模型的检验
    delta = results_AR.fittedvalues - temp[17:]  # 残差
    plt.figure(figsize=(10, 6))
    # plt.plot(temp[17:],label='original value')
    # plt.plot(results_AR.fittedvalues,label='fitted value')
    plt.plot(delta, 'r', label=' residual error')
    plt.legend(loc=0)
    #
    acf, q, p = sm.tsa.acf(delta, nlags=10, qstat=True)  ## 计算自相关系数 及p-value
    out = np.c_[range(1, 11), acf[1:], q, p]
    output = pd.DataFrame(out, columns=['lag', "AC", "Q", "P-value"])
    output = output.set_index('lag')
    print(output)

    # 拟合优度以及预测
    score = 1 - delta.var() / temp[17:].var()
    print(score)
    plt.show()

    train = temp[:-10]
    test = temp[-10:]
    output = sm.tsa.AR(train).fit()
    output.predict()

    predicts = output.predict(355, 364, dynamic=True)
    print(len(predicts))
    comp = pd.DataFrame()
    comp['original'] = temp[-10:]
    comp['predict'] = predicts
    print(comp)


def _main():
    initialize()
    ts_analysis()


if __name__ == '__main__':
    _main()

#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: arima_demo.py
@time: 2021/1/18 16:47
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


def retrive_ts_data(intraday=False, metric=None):
    if intraday:
        df_mkt = pd.read_csv('../data/000021.csv')
        df_mkt.sort_values(by=['dataDate', 'barTime'], inplace=True)
        df_mkt = df_mkt[df_mkt.dataDate == '2019-03-20']
        df_mkt = df_mkt.set_index(df_mkt['barTime'])
        _col_name = metric or 'closePrice'
        data2 = df_mkt['closePrice']  #
    else:
        df_index = DataAPI.MktIdxdGet(indexID=u"", ticker=u"000001", beginDate=u"20130101", endDate=u"20140801",
                                      field=u"tradeDate,closeIndex,CHGPct", pandas="1")
        df_index = df_index.set_index(df_index['tradeDate'])
        _col_name = metric or 'closeIndex'
        data2 = df_index['closeIndex']  # 上证指数
    return data2


def adf_test(ts_inputs=[]):
    temp = np.array(ts_inputs)[1:]
    t = sm.tsa.stattools.adfuller(temp)  # ADF检验
    output = pd.DataFrame(
        index=['Test Statistic Value', "p-value", "Lags Used", "Number of Observations Used", "Critical Value(1%)",
               "Critical Value(5%)", "Critical Value(10%)"], columns=['value'])
    output['value']['Test Statistic Value'] = t[0]
    output['value']['p-value'] = t[1]
    output['value']['Lags Used'] = t[2]
    output['value']['Number of Observations Used'] = t[3]
    output['value']['Critical Value(1%)'] = t[4]['1%']
    output['value']['Critical Value(5%)'] = t[4]['5%']
    output['value']['Critical Value(10%)'] = t[4]['10%']
    pprint.pprint(output)

    data2Diff = ts_inputs.diff()  # 差分
    data2Diff.plot(figsize=(15, 5))

    temp = np.array(data2Diff)[1:]  # 差分后第一个值为NaN,舍去
    t = sm.tsa.stattools.adfuller(temp)  # ADF检验
    print("p-value:   ", t[1])


def order_dertimin(ts_inputs=[]):
    data2Diff = ts_inputs.diff()  # 差分
    # # 模型阶次确定
    temp = np.array(data2Diff)[1:]  # 差分后第一个值为NaN,舍去
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(temp, lags=20, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(temp, lags=20, ax=ax2)


def model_training(ts_inputs=[]):
    data2Diff = ts_inputs.diff()  # 差分
    temp = np.array(data2Diff)[1:]  # 差分后第一个值为NaN,舍去
    ret = sm.tsa.arma_order_select_ic(temp, max_ar=6, max_ma=5, ic='aic')  # AIC
    print("aic result", ret.aic_min_order)

    order = (2, 2)
    data = np.array(data2Diff)[1:]  # 差分后，第一个值为NaN
    rawdata = np.array(ts_inputs)
    train = data[:-10]
    test = data[-10:]
    model = sm.tsa.ARMA(train, order).fit()
    #
    plt.figure(figsize=(15, 5))
    plt.plot(model.fittedvalues, label='fitted value')
    plt.plot(train[1:], label='real value')
    plt.legend(loc=0)

    delta = model.fittedvalues - train
    score = 1 - delta.var() / train[1:].var()
    print(score)

    predicts = model.predict(10, 381, dynamic=True)[-10:]
    print(len(predicts))
    comp = pd.DataFrame()
    comp['original'] = test
    comp['predict'] = predicts
    comp.plot(figsize=(8, 5))

    rec = [rawdata[-11]]
    pre = model.predict(371, 380, dynamic=True)  # 差分序列的预测
    for i in range(10):
        rec.append(rec[i] + pre[i])
    plt.figure(figsize=(10, 5))
    plt.plot(rec[-10:], 'r', label='predict value')
    plt.plot(rawdata[-10:], 'blue', label='real value')
    plt.legend(loc=0)


def _main():
    initialize()
    ts_raw = retrive_ts_data(intraday=False)
    adf_test(ts_raw)
    plt.show()


if __name__ == "__main__":
    _main()

#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: ma_demo.py
@time: 2021/1/18 16:28
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
    IndexData = DataAPI.MktIdxdGet(indexID=u"", ticker=u"000001", beginDate=u"20130101", endDate=u"20140801",
                                   field=u"tradeDate,closeIndex,CHGPct", pandas="1")
    IndexData = IndexData.set_index(IndexData['tradeDate'])
    data = np.array(IndexData['CHGPct'])
    IndexData['CHGPct'].plot(figsize=(15, 5))

    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(111)
    fig = sm.graphics.tsa.plot_acf(data, ax=ax1)

    order = (0, 10)
    train = data[:-10]
    test = data[-10:]
    tempModel = sm.tsa.ARMA(train, order).fit()

    delta = tempModel.fittedvalues - train
    score = 1 - delta.var() / train.var()
    print(score)

    predicts = tempModel.predict(371, 380, dynamic=True)
    print(len(predicts))
    comp = pd.DataFrame()
    comp['original'] = test
    comp['predict'] = predicts
    comp.plot()
    plt.show()


def _main():
    initialize()
    ts_analysis()


if __name__ == '__main__':
    _main()

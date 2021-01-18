#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: arma_demo.py
@time: 2021/1/18 16:28
@desc:
'''

import pprint
import numpy as np
import pandas as pd
import uqer
from uqer import DataAPI
import matplotlib.pyplot as plt

from scipy import stats
import statsmodels.api as sm

with open('conf') as f:
    t = f.readline()
    uqer_client = uqer.Client(token=t)

IndexData = DataAPI.MktIdxdGet(indexID=u"", ticker=u"000001", beginDate=u"20130101", endDate=u"20140801",
                               field=u"tradeDate,closeIndex,CHGPct", pandas="1")
IndexData = IndexData.set_index(IndexData['tradeDate'])
data = np.array(IndexData['CHGPct'])  # 上证指数日涨跌

fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data, lags=30, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data, lags=30, ax=ax2)

# 通过信息准则定阶
print("AIC", sm.tsa.arma_order_select_ic(data, max_ar=6, max_ma=4, ic='aic')['aic_min_order'])  # AIC
print("BIC", sm.tsa.arma_order_select_ic(data, max_ar=6, max_ma=4, ic='bic')['bic_min_order'])  # BIC
print("HQIC", sm.tsa.arma_order_select_ic(data, max_ar=6, max_ma=4, ic='hqic')['hqic_min_order'])  # HQIC

# 模型建立
order = (3, 2)
train = data[:-10]
test = data[-10:]
tempModel = sm.tsa.ARMA(train, order).fit()

# 拟合效果
delta = tempModel.fittedvalues - train
score = 1 - delta.var() / train.var()
print(score)

# 预测效果
predicts = tempModel.predict(371, 380, dynamic=True)
print(len(predicts))
comp = pd.DataFrame()
comp['original'] = test
comp['predict'] = predicts
comp.plot()

# -*- coding:utf-8 -*-
"""
Project: Question2.py
Written by: Evan Wong
DATE: 2023/5/12
TIME: 20:37
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import itertools
from scipy.stats import normaltest


# 假设已经收集了江苏省历史碳排放数据，这里将其表示为一个字典
carbon_emission_data = {
    'year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
    'emission': [1000, 1100, 1200, 1300, 1350, 1400, 1420, 1440, 1450, 1460, 1470, 1480]
}

# 将数据转换为DataFrame格式
df = pd.DataFrame(carbon_emission_data)
df['year'] = pd.to_datetime(df['year'], format='%Y')
df.set_index('year', inplace=True)

# 平稳性检验（ADF检验）
result = adfuller(df['emission'])
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

# 对数变换
df['log_emission'] = np.log(df['emission'])

# 一阶差分
df['log_emission_diff'] = df['log_emission'].diff()
df.dropna(inplace=True)

# 重新进行ADF检验，检查差分后的数据是否平稳
result = adfuller(df['log_emission_diff'])
print(f'ADF Statistic after differencing: {result[0]}')
print(f'p-value after differencing: {result[1]}')

# 可视化原始数据和差分后的数据
plt.figure(figsize=(12, 6))
plt.subplot(211)
plt.plot(df['emission'])
plt.title('Original Emission Data')
plt.subplot(212)
plt.plot(df['log_emission_diff'])
plt.title('Differenced Log Emission Data')
plt.show()

# ACF和PACF图
plot_acf(df['log_emission_diff'])
plt.title('ACF')
plot_pacf(df['log_emission_diff'], lags=4.99)
plt.title('PACF')

# 确定参数范围
p_range = range(0, 3)
d_range = range(0, 2)
q_range = range(0, 3)

# 计算所有参数组合的AIC
best_aic = float('inf')
best_order = None

for p, d, q in itertools.product(p_range, d_range, q_range):
    if p == 0 and d == 0 and q == 0:
        continue

    try:
        model = ARIMA(df['log_emission'], order=(p, d, q))
        results = model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_order = (p, d, q)
    except:
        continue

print(f'Best ARIMA parameters: {best_order}, AIC: {best_aic}')

# 使用最佳参数拟合ARIMA模型
model = ARIMA(df['log_emission'], order=best_order)
results = model.fit()

# 输出模型摘要信息
print(results.summary())

# 计算预测残差
residuals = results.resid

# 绘制残差图
plt.figure(figsize=(12, 6))
plt.plot(residuals)
plt.title('Residuals')
plt.show()

# 计算均方误差
mse = mean_squared_error(df['log_emission_diff'][1:], residuals)
print(f'Mean Squared Error: {mse}')

# 残差正态性检验
stat, p = normaltest(residuals)
print(f'Normality Test p-value: {p}')

# 如果需要调整模型参数，可以返回到步骤3，并尝试其他参数组合。

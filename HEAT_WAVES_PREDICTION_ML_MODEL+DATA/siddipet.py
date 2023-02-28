# -*- coding: utf-8 -*-
"""SIDDIPET.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B4pCNESYQvTEmo94Zh4ncih1F2HhEQir
"""

import pandas as pd
dataset_siddipet=pd.read_csv('/content/siddipet_dataset_final.csv')

dataset_siddipet.head()

dataset_siddipet[10:]

dataset_siddipet['Date'] = pd.to_datetime(dataset_siddipet['Date'])

dataset_siddipet[10:]

dataset_siddipet['Date'] =dataset_siddipet['Date'].dt.date

dataset_siddipet.shape

avg_by_date = dataset_siddipet.groupby('Date')['temp_max (⁰C)'].mean()

avg_by_date=avg_by_date.to_frame()

avg_by_date.shape

avg_by_date.head()

avg_by_date=avg_by_date.reset_index()

avg_by_date.info()

avg_by_date['Date'] = pd.to_datetime(avg_by_date['Date'])

from statsmodels.tsa.stattools import adfuller
def adf_test(result):
  ndt=adfuller(result,autolag='AIC')
  print("1 ADF :",ndt[0])
  print("2 p val:",ndt[1])
  print("3 lags",ndt[2])
  print("4 no. of observations",ndt[3])
  print("5 critical value")
  for key,val in ndt[4].items():
    print("\t",key," ",val)

!pip install pmdarima

!pip install pyfiglet

from pmdarima import auto_arima
import statsmodels.api as sm
import pyfiglet

dataset=[]

# create a list of dataframes, one for each month
dfs = []
for i in range(1, 13):
    mask = (avg_by_date['Date'].dt.month == i)
    dfs.append(avg_by_date.loc[mask])

# print the resulting dataframes
for i, month_df in enumerate(dfs):
    adf_test(month_df['temp_max (⁰C)'])
    arimadata=auto_arima(month_df['temp_max (⁰C)'],trace=True)
    train=month_df.iloc[:-30]
    test=month_df.iloc[-30:]
    model=sm.tsa.arima.ARIMA(train['temp_max (⁰C)'],order=(1,0,5))
    model=model.fit()
    s=len(train)
    e=len(train)+len(test)-1
    pred=model.predict(start=s,end=e,typ='levels').rename('ARIMA Predictions')
    dataset.append(pred)

len(dataset)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

for i in range(0,12):
  dataset[i]=dataset[i].to_frame()

dates = pd.date_range(start='2023-01-01', end='2023-01-30', freq='D')
dataset[0]['Dates']=dates

dates = pd.date_range(start='2023-02-01', end='2023-02-28', freq='D')
# Drop the last two rows of the DataFrame
dataset[1] = dataset[1].drop(index=dataset[1].index[-2:])
dataset[1]['Dates']=dates

dates = pd.date_range(start='2023-03-01', end='2023-03-30', freq='D')
dataset[2]['Dates']=dates

dates = pd.date_range(start='2023-04-01', end='2023-04-30', freq='D')
dataset[3]['Dates']=dates

dates = pd.date_range(start='2023-05-01', end='2023-05-30', freq='D')
dataset[4]['Dates']=dates

dates = pd.date_range(start='2023-06-01', end='2023-06-30', freq='D')
dataset[5]['Dates']=dates

dates = pd.date_range(start='2023-07-01', end='2023-07-30', freq='D')
dataset[6]['Dates']=dates

dates = pd.date_range(start='2023-08-01', end='2023-08-30', freq='D')
dataset[7]['Dates']=dates

dates = pd.date_range(start='2023-09-01', end='2023-09-30', freq='D')
dataset[8]['Dates']=dates

dates = pd.date_range(start='2023-10-01', end='2023-10-30', freq='D')
dataset[9]['Dates']=dates

dates = pd.date_range(start='2023-11-01', end='2023-11-30', freq='D')
dataset[10]['Dates']=dates

dates = pd.date_range(start='2023-12-01', end='2023-12-30', freq='D')
dataset[11]['Dates']=dates

dataset[0].info()

"""The India Meteorological Department (IMD) declares a heatwave when the maximum temperature in a particular location reaches or exceeds a threshold value, which varies depending on the location. The threshold values for a heatwave are typically defined as temperatures that are significantly higher than the average maximum temperature for that location during the summer season."""

mean_temp=dataset[4]['ARIMA Predictions'].mean()
print(mean_temp)

mean_temp=dataset[3]['ARIMA Predictions'].mean()
print(mean_temp)

normal_temp =(37.87149008253771+39.20472015403835)/2  # Mean maximum temperature in Celsius for the hottest month

print(normal_temp)

for i in range(0,12):
  for index, row in dataset[i].iterrows():
    diff = row['ARIMA Predictions'] - normal_temp   
    if row['ARIMA Predictions'] >= 40:
       print("Severe Heat Wave on {} when temperature is {}".format(row['Dates'].date(),row['ARIMA Predictions']))
    elif row['ARIMA Predictions'] >= 38.5:
        print("Heat Wave on {} when temperature is {}".format(row['Dates'].date(),row['ARIMA Predictions']))
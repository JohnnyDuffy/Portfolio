## This is a script to compare any number of cryptocurrencies, comparing their correlation and relative price movement


import numpy as np
import pandas as pd
import pandas_datareader as web
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing

#Specify date Range
start = datetime(2021,1,1)
end = datetime.today()

#Specify which cryptocurrencies to analyse
currencies = ['BTC','ETH','BNB','ADA','XRP']

#Reformat to be readable by DataReader
tickers = []
for elem in currencies: 
    tickers.append(elem + '-USD')

#Fetch live prices
prices = web.DataReader(tickers,'yahoo',start,end)['Adj Close']


# 1. Scaled Prices

#Scale the prices
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))
scaled_prices = min_max_scaler.fit_transform(prices)
#Convert to dataframe
scaled_prices = pd.DataFrame(scaled_prices, columns = prices.columns)
#plot scaled data
plt.figure(figsize=(10,8))
plt.subplot(2,1,1)
for c in scaled_prices.columns.values:
   plt.plot(prices.index,scaled_prices[c], label=c)

plt.title('Cryptocurrency Scaled Graph')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.ylabel('Scaled Price')
plt.legend(currencies, loc = 'upper left')


# 2. Correlation Heatmap
plt.subplot(2,2,3)
correlation = prices.corr()
sns.heatmap(correlation,annot=True,cmap='Blues', xticklabels=currencies,yticklabels=currencies)
plt.title('Cryptocurrency correlations')


plt.subplot(2,2,4)
# 3. Daily Cumulative Simple Return
# This can be replaced by a simple bar chart by replacing with the commented code below

DSR = prices.pct_change(1)  #Daily simple return
DCSR = (DSR+1).cumprod()  #Daily cumulative simple return
for c in DCSR.columns.values:
    plt.plot(DCSR.index,DCSR[c],label=c)
plt.title('Daily Cumulative Simple Return')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.ylabel('Growth of $1 investment')
plt.legend(currencies, loc = 'upper left', fontsize = 10)

# -- Replace the above code with the following to use a simple bar chart instead:

# for c in prices.columns.values:
#     if c == 'Date': continue
#     ratio = float(prices[c].iloc[-1]) / float(prices[c].iloc[0]) *100
#     plt.bar(c,ratio)
# plt.title('Return on Investment')
# plt.ylabel('% Return')
# plt.xticks(rotation=45)



plt.subplots_adjust(wspace=.4,hspace=.5)
plt.show()
#        This program is able to take live price data for user specified assets, and return a single portfolio with optimised weighting

import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime
from matplotlib import pyplot as plt
from resources.Functions import return_portfolios, optimal_portfolio  #These functions were not written by myself, but taken from an online resource

# Specify timeframe
start = datetime(2017,9,30)
end = datetime.today()


# Specify assets
Stocks = ['AMZN','AAPL']
Crypto = ['BTC-USD','ETH-USD','LTC-USD']



# Retrieve price data 
stock_data = web.get_data_yahoo(Stocks,start,end)
crypto_data = web.get_data_yahoo(Crypto,start,end)



# Combine dataframes and convert to quarterly prices
combined = stock_data['Adj Close'].join(crypto_data['Adj Close'])
Q_prices = combined.resample('Q').ffill()


# Calculate returns, then expected returns and covariance
Q_returns = Q_prices.pct_change()        

expected_returns = Q_returns.mean()
cov_matrix = Q_returns.cov()


# Generate portfolios and calculate optimal solution
prt=return_portfolios(expected_returns, cov_matrix)
weights, returns, risks = optimal_portfolio(Q_returns[1:])




#Print optimised portfolio weights
print('')
weights *= 100
tickers = Stocks + Crypto
for i in range(len(tickers)):
  print('{0:.1f}% {1}'.format(float(weights[i]), tickers[i]))
  
#Plot data
prt.plot.scatter(x='Volatility', y='Returns')
plt.plot(risks, returns, 'y-o')
plt.title('Portfolios beginning at {0}, until today'.format(start.date()))
plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
from datetime import datetime


# Specify time period
start = datetime(2018,1,1)
end = datetime.today()

# Retrieve price data
data = web.DataReader('BTC-USD','yahoo',start,end)
data = data[['Adj Close']]


# Set moving average window sizes
short_term_window_size = 10
long_term_window_size = 40

# Calculate and store the rolling averages in their own columns
data.loc[:, 'window_ST'] = data['Adj Close'].rolling(
    short_term_window_size).mean()

data.loc[:, 'window_LT'] = data['Adj Close'].rolling(
    long_term_window_size).mean()


# Plot short and longterm averages against bitcoin price
f = plt.figure(figsize=(11,8))
ax = f.add_subplot(211)
ax2 = f.add_subplot(212)
ax.plot(data)
ax.set_title('Short and Long Term Averages')
ax.set_ylabel('Price')
ax.grid(which="major", color='k', linestyle='-.', linewidth=0.2)


# Compare the value of short term and long term window and set buy or sell signal at each point
data.loc[:, 'signal'] = np.where(data['window_ST'] > data['window_LT'], 1, -1)

# Apply the signal on the next day
data.loc[:, 'signal'] = data['signal'].shift(1)

# Replace NaN values with 0
data.loc[:, 'signal'] = data['signal'].replace(np.nan, 0)


# Calculate the returns by multiplying the signal with daily price change
returns = data['signal']*data['Adj Close'].pct_change()



# Factor in commission cost, and apply to returns
cost = (0.001 * np.abs(data['signal'] - data['signal'].shift(-1)))

returns -= cost


# Calculate cumulative returns of the strategy, and plot against simply HODLing
cumulative_returns = (returns+1).cumprod()
ax2.plot(cumulative_returns)  # Strategy

ax2.plot((data['Adj Close'].pct_change()+1).cumprod())  # HODL

ax2.legend(['moving average strategy', 'buy&hold'])
ax2.set_title('Value of $1 invested')
ax2.set_ylabel('$ Value')
ax2.grid(which="major", color='k', linestyle='-.', linewidth=0.2)
plt.show()


# Print final statistics
print('')
print('Strategy Returns: ', (returns+1).prod() )

market_returns = ((data['Adj Close'][-1] - data['Adj Close'][0]) / data['Adj Close'][0]) + 1
print('  Market returns: ', market_returns)
print('')
print('Improvement on Market: ', ((returns+1).prod() - market_returns) *100, '%')

# Calculate and show Sharpe Ratio
print('         Sharpe Ratio: ', (returns.mean()/returns.std())*(365)**(1/2) )

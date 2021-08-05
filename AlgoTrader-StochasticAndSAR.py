## This is a simple bitcoin trading bot that generates buy and signals based of the calculated SAR and Stochastic Oscillator values. Although it needs tweaking to be more profitable.

import numpy as np
import pandas as pd
import pandas_datareader as web
import talib as ta
import matplotlib.pyplot as plt
from datetime import datetime

# Retrieve Data
start = datetime(2021,1,1)
end = datetime.today()
df = web.DataReader('BTC-USD','yahoo',start,end)

# Calculate Parabolic SAR
df['SAR'] = ta.SAR(df.High.values, df.Low.values, acceleration = 0.02, maximum = 0.2 )

# Calculate Stochastic Oscillator
df['fastk'], df['fastd'] = ta.STOCHF(df.High.values, df.Low.values, df.Close.values, fastk_period = 5, fastd_period = 3)
df['slowk'], df['slowd'] = ta.STOCH(df.High.values, df.Low.values, df.Close.values, fastk_period = 5, slowk_period = 3, slowd_period = 3)

# Build signal column
df['signal'] = np.nan

# Generate buy and sell signals
df.loc[ (df.SAR < df.Close) & (df.fastd > df.slowd) & (df.fastk > df.slowk), 'signal' ] = 1   # Buy Signal
df.loc[ (df.SAR > df.Close) & (df.fastd < df.slowd) & (df.fastk < df.slowk), 'signal' ] = -1  # Sell Signal

# Fill in signal column
df = df.fillna(method = 'ffill')

# Calculate regular returns
df['returns'] = df.Close.pct_change()  

# Calculate strategy returns
df['strategy_returns'] = df.returns * df.signal.shift(1)

# Remove rows with NaN values
df = df.dropna()



# Build plot framework
f, (a0, a1) = plt.subplots(2,1, gridspec_kw={'height_ratios': [3, 1]})
f.set_figheight(10)
f.set_figwidth(14)

# Plot Returns
a0.plot((df.returns+1).cumprod(), color = 'orange')
a0.plot((df.strategy_returns+1).cumprod(), color = 'green')
a0.legend(['Regular','strategy'])
a0.grid(linestyle = '--')

# Plot Stochastic Oscillator
a1.plot(df.fastk, color='blue')
a1.plot(df.slowd, color='orange')
plt.axhline(80, color='black')
plt.axhline(20, color='black')
a1.grid(axis='x', linestyle = '--')

plt.show()

# This script takes data from honey producers in the US, analyses average output per year, and uses regression to extrapolate a trendline out.


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

df = pd.read_csv("resources/honeyproduction.csv")

# Group the data by year, and find the mean for each
prod_per_year = df.groupby('year').totalprod.mean().reset_index()

# Extract the year values and reshape it to vertical
x = prod_per_year['year']
x = x.values.reshape(-1, 1)

y = prod_per_year['totalprod']

plt.scatter(x,y)

# Generate linear regression model
regr = linear_model.LinearRegression()
regr.fit(x,y)

#Calculate line of best fit and plot
y_predict = regr.predict(x)
plt.plot(x,y_predict, color='green')


# Extrapolate data into future 
x_future = np.array(range(2013, 2031))
x_future = x_future.reshape(-1, 1)

future_predict = regr.predict(x_future)
plt.plot(x_future,future_predict,color = 'red')



plt.title('Honey Production over Time')
plt.ylabel('Total Production (lbs)')
plt.xlabel('Date')
plt.show()

#     This is a function to analyse stock data from two CSV files, containing adjusted daily closes. Here using data from two Real Estate Investment Trusts (REITs).

# The class is capable of calculating annualised returns, variance, standard deviation, and the correlation with another stock.

# The class makes it possible to calculate this data with either the simple rate of return or the log rate, but will default to the log rate.
# to change to simple, add 'simple' as a method argument.





import numpy as np

class stock():
    def __init__(self,adj_closings):
        self.adj_closings = adj_closings


    def simple_rate_of_return(self):
        self.daily_simple_ror = np.diff(self.adj_closings)/self.adj_closings[:-1]
        return self.daily_simple_ror
    
    def daily_log_returns(self):
        __log_adj_closings = np.log(self.adj_closings)
        self.d_log_returns = np.diff(__log_adj_closings)
        return self.d_log_returns
    
    def annualised_daily_returns(self,__LogOrSimple = 'log'):
        if __LogOrSimple == 'log' :
            return np.mean(self.daily_log_returns()) * 252
        if __LogOrSimple == 'simple' :
            return np.mean(self.simple_rate_of_return()) * 252
        else: return 'invalid input'

    def variance(self,__LogOrSimple = 'log'):
        if __LogOrSimple == 'log' :
            return np.var(self.daily_log_returns())
        if __LogOrSimple == 'simple' :
            return np.var(self.simple_rate_of_return()) 
        else: return 'invalid input'
    
    def standard_deviation(self,__LogOrSimple = 'log'):
        if __LogOrSimple == 'log' :
            j = np.std(self.daily_log_returns())
            return j

        if __LogOrSimple == 'simple' :
            return np.std(self.simple_rate_of_return()) 
        else: return 'invalid input'
    
    def correlation(self, SecondStock, __LogOrSimple = 'log'):
        if __LogOrSimple == 'log' :
            return np.corrcoef(self.daily_log_returns(),SecondStock.daily_log_returns())
        if __LogOrSimple == 'simple' :
            return np.corrcoef(self.simple_rate_of_return(),SecondStock.simple_rate_of_return()) 
        else: return 'invalid input'






#import adjusted closings data for the two stocks, and assign them to the class

SBRA_adj_closings = np.loadtxt('SBRA.csv', skiprows=1, usecols=5,delimiter = ',')
EQR_adj_closings = np.loadtxt('EQR.csv', skiprows=1, usecols=5,delimiter = ',')

SBRA = stock(SBRA_adj_closings)
EQR = stock(EQR_adj_closings)




print('''
                            |    SBRA    |    EQR    |
                            --------------------------
      Annualised Returns    |   {0:.3f}    |   {1:.3f}   |
                            |------------|-----------|
                Variance    |   {2:.4f}   |   {3:.4f}  |
      Standard Deviation    |   {4:.3f} %  |   {5:.3f} % |

             Correlation:   {6:.3f}         

    '''.format(
        SBRA.annualised_daily_returns(),
        EQR.annualised_daily_returns(),
        SBRA.variance(),
        EQR.variance(),
        (SBRA.standard_deviation() * 100),   #changing standard deviation to a percentage
        (EQR.standard_deviation() * 100),
        SBRA.correlation(EQR)[0][1]          #taking the coefficient out of the array
        )
    

    )

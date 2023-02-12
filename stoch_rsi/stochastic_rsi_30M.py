#!/usr/bin/env python
# coding: utf-8

# In[8]:


# import numpy as np
# import pandas as pd


# In[9]:


# # The function to add a certain number of columns
# def adder(Data, times):
    
#     for i in range(1, times + 1):
    
#         z = np.zeros((len(Data), 1), dtype = float)
#         Data = np.append(Data, z, axis = 1)            
#     return Data

# # The function to delete a certain number of columns
# def deleter(Data, index, times):
    
#     for i in range(1, times + 1):
    
#         Data = np.delete(Data, index, axis = 1)            
#     return Data

# # The function to delete a certain number of rows from the beginning
# def jump(Data, jump):
    
#     Data = Data[jump:, ]
    
#     return Data


# In[10]:


# def ma(Data, lookback, what, where):
    
#   for i in range(len(Data)):
#     try:
#         Data[i, where] = (Data[i - lookback + 1:i + 1, what].mean())
#     except IndexError:
#         pass
#     return Data

# def ema(Data, alpha, lookback, what, where):

#     # alpha is the smoothing factor
#     # window is the lookback period
#     # what is the column that needs to have its average calculated
#     # where is where to put the exponential moving average

#     alpha = alpha / (lookback + 1.0)
#     beta  = 1 - alpha
    
#     # First value is a simple SMA
#     Data = ma(Data, lookback, what, where)
    
#     # Calculating first EMA
#     Data[lookback + 1, where] = (Data[lookback + 1, what] * alpha) + (Data[lookback, where] * beta)
#     # Calculating the rest of EMA
#     for i in range(lookback + 2, len(Data)):
#             try:
#                 Data[i, where] = (Data[i, what] * alpha) + (Data[i - 1, where] * beta)
        
#             except IndexError:
#                 pass
#     return Data

    


# In[11]:


# def rsi(Data, rsi_lookback, what1, what2):
#     # Data: This is the data of the stock's price history.
#     # rsi_lookback: This is the number of days to look back when calculating the RSI.
#     # what1: This is the index of the data in the Data array to be used as the stock price.
#     # what2: This is the index of the data in the Data array to be used in the adder and ema functions.

#     # From exponential to smoothed
#     rsi_lookback = (rsi_lookback * 2) - 1  
        
#     # Get the difference in price from previous step
#     delta = []
   
#     for i in range(len(Data)):
#         try:
#             diff = Data[i, what1] - Data[i - 1, what1] 
#             delta = np.append(delta, diff)                  
#         except IndexError:
#             pass
        
#     delta = np.insert(delta, 0, 0, axis = 0)               
#     delta = delta[1:] 

#     # Make the positive gains (up) and negative gains (down) Series
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
    
#     up = np.array(up)
#     down = np.array(down)
    
#     roll_up = up
#     roll_down = down

#     # Reshaping the roll_up an roll_down to size (-1, 1) meaning 1 column and n rows 
#     roll_up = np.reshape(roll_up, (-1, 1))
#     roll_down = np.reshape(roll_down, (-1, 1))

#     # adder and ema to calculate ema of up and down
#     roll_up = adder(roll_up, 3)
#     roll_down = adder(roll_down, 3)
    
#     roll_up = ema(roll_up, 2, rsi_lookback, what2, 1)
#     roll_down = ema(abs(roll_down), 2, rsi_lookback, what2, 1)
    
#     # remove the initial data points that do not have sufficient data to calculate the RSI
#     roll_up = roll_up[rsi_lookback:, 1:2]
#     roll_down = roll_down[rsi_lookback:, 1:2]
#     Data = Data[rsi_lookback + 1:,]
    
#     # Calculate the RS & RSI
#     RS = roll_up / roll_down
#     RSI = (100.0 - (100.0 / (1.0 + RS)))
#     RSI = np.array(RSI)
#     RSI = np.reshape(RSI, (-1, 1))
#     RSI = RSI[1:,]
    
#     Data = np.concatenate((Data, RSI), axis = 1)    
#     return Data


# In[12]:


# def stochastic(Data, lookback, what, high, low, where):
        
#     for i in range(len(Data)):
        
#         try:
#           Data[i, where] = (Data[i, what] - min(Data[i - lookback + 1:i + 1, low])) / (max(Data[i - lookback + 1:i + 1, high]) - min(Data[i - lookback + 1:i + 1, low]))
        
#         except ValueError:
#             pass
    
#     Data[:, where] = Data[:, where] * 100            
#     return Data
    
# # The Data variable refers to the OHLC array
# # The lookback variable refers to the period (5, 14, 21, etc.)
# # The what variable refers to the closing price
# # The high variable refers to the high price
# # The low variable refers to the low price
# # The where variable refers to where to put the Oscillator


# In[13]:


# def stoch_rsi(Data, lookback, where):
    
#     # Calculating RSI of the Closing prices
#     Data = rsi(Data, lookback, 3, 0)
    
#     # Adding two columns
#     Data = adder(Data, 2)
    
#     for i in range(len(Data)):
        
#         try:
#             Data[i, where + 1] = (Data[i, where] - min(Data[i - lookback + 1:i + 1, where])) / (max(Data[i - lookback + 1:i + 1, where]) - min(Data[i - lookback + 1:i + 1, where]))
        
#         except ValueError:
#             pass
    
#     Data[:, where + 1] = Data[:, where + 1] * 100 
    
#     # Signal Line using a 3-period moving average
#     Data = ma(Data, 3, where + 1, where + 2)
    
#     Data = deleter(Data, where, 2)
#     Data = jump(Data, lookback)    
    
#     return Data


# In[14]:


# my_data = None
# lookback = 14


# In[15]:


# my_data = rsi(my_data, lookback, 3, 0)
# my_data = stoch_rsi(my_data, 14, 4)


# In[28]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime
import time


# In[18]:


df = pd.read_csv(r"Z:\\projects\\ez_money\\raw_data_30m\\EURUSD_M30.csv", sep='\t')


# In[35]:


df = df[:500]
df


# In[19]:


def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[diff > 0]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[diff < 0]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi


# In[36]:


df['RSI'] = computeRSI(df['Close'], 14)


# In[37]:


df


# In[22]:


def stochastic(data, k_window, d_window, window):
    
    # input to function is one column from df
    # containing closing price or whatever value we want to extract K and D from
    
    min_val  = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()
    
    stoch = ( (data - min_val) / (max_val - min_val) ) * 100
    
    K = stoch.rolling(window=k_window, center=False).mean() 
    #K = stoch
    
    D = K.rolling(window=d_window, center=False).mean() 


    return K, D
    


# In[38]:


# The "K" line is a fast moving average and is calculated as follows: K = 100 * (RSI - RSI min) / (RSI max - RSI min)

# The "D" line is a slow moving average of the K line and is used as a signal line to identify overbought and oversold conditions. 
# The D line is calculated using a simple moving average or exponential moving average of the K line.

df['K'], df['D'] = stochastic(df['RSI'], 3, 3, 14)


# In[39]:


df


# In[31]:


# Plotting
def plot_price(df):
    # plot price
    plt.figure(figsize=(15,5))
    plt.plot(df['Close'])
    plt.title('Price chart (Close)')
    plt.show()
    return None

def plot_RSI(df):
    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('RSI chart')
    plt.plot(df['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
    return None

def plot_stoch_RSI(df):
    # plot corresponding Stoch RSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('stochRSI chart')
    plt.plot(df['K'])
    plt.plot(df['D'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    #plt.axhline(30, linestyle='--')

    #plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
    return None


# In[41]:


def plot_all(df):
    plot_price(df)
    #plot_RSI(df)
    plot_stoch_RSI(df)
    return None


# In[42]:


plot_all(df)


# In[43]:


df.to_csv('Z:\projects\ez_money\pre_processed_data\stochrsi\\eurusd_m30_stochrsi.csv')


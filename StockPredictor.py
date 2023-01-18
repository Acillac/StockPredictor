#!/usr/bin/env python
# coding: utf-8

# In[5]:


import yfinance as yf
import numpy as np 
import matplotlib.pyplot as plt 
import math
import statistics
import scipy.stats as st


# In[8]:


stock_tag = input("Input stock ticker: ")
history_basis = input("Input in years how much data the prediction is based on: ")
future = input("How many trading days from now would you like to calculate for: ")
certainity = input("With how much certainty would you like the range of the mean to be: ")


# In[11]:


df = yf.download(stock_tag)

adj_close = df['Adj Close']
if int(history_basis) * 252 < len(adj_close):
    adj_close = adj_close[-(252 * int(history_basis)):]

returns = np.log(1+ adj_close.pct_change()) 
mu, sigma= returns.mean(), returns.std() 
initial = adj_close.iloc[-1] 
mylist = []
for i in range(500):
    sim_rets=np.random.normal(mu, sigma, int(future)) 
    sim_prices=initial*(sim_rets+1).cumprod() 
    plt.axhline(initial, color='k') 
    plt.plot(sim_prices) 
    plt.ylabel("price")
    plt.xlabel("days")
    pyval = sim_prices[int(future) - 1].item()
    mylist.append(pyval)
    
mean = np.mean(mylist)
std_dev = statistics.stdev(mylist) 
low, high = st.norm.interval(alpha=int(certainity) / 100, loc=mean, scale=st.sem(mylist))
plt.axhline(low, color = 'red')
plt.axhline(high, color = 'green')
plt.axhline(mean, color = 'black')

print("{} will result in an average of ${} gain to ${} gain after {} days with {}% certainity.".format(stock_tag, str(low - initial), str(high - initial), future, certainity))







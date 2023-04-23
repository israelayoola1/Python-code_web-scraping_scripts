#!/usr/bin/env python
# coding: utf-8

# In[1]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '17bd8fd7-f674-40ce-b1b5-03c208a05e33',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[2]:


type(data)


# In[3]:


import pandas as pd


#This allows you to see all the columns, not just like 15
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[4]:


#This normalizes the data and makes it all pretty in a dataframe

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[5]:


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
    #Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '17bd8fd7-f674-40ce-b1b5-03c208a05e33',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

#NOTE:
# I had to go in and put "jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10"
# Into the Anaconda Prompt to change this to allow to pull data
    
 # Use this if you want to create a csv and append data to it
    #df = pd.json_normalize(data['data'])
    #df['timestamp'] = pd.to_datetime('now')
    #df

    #if not os.path.isfile(r'C:\Users\Latitude E5440\Documents\Python Scripts\API.csv'):
        #df.to_csv(r'C:\Users\Latitude E5440\Documents\Python Scripts\API.csv', header='column_names')
    #else:
        #df.to_csv(r'C:\Users\Latitude E5440\Documents\Python Scripts\API.csv', mode='a', header=False)
        
    #Then to read in the file: df = pd.read_csv(r'C:\Users\Latitude E5440\Documents\Python Scripts\API.csv')


# In[6]:


import os 
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(60) #sleep for 1 minute
exit()


# In[7]:


# One thing I noticed was the scientific notation. I like it, but I want to be able to see the numbers in this case

pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[49]:


df


# In[8]:


# Now let's look at the coin trends over time

df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3


# In[9]:


df4 = df3.stack()
df4


# In[10]:


type(df4)


# In[11]:


df5 = df4.to_frame(name='values')
df5


# In[12]:


df5.count()


# In[13]:


index = pd.Index(range(90))

# Set the above DataFrame index object as the index
# using set_index() function
df6 = df5.set_index(index)
df6


# In[14]:


# Change the column name

df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[15]:


df7 = pd.read_json('https://api.coinmarketcap.com/v1/ticker/?limit=100')
df7 = df7.assign(
    percent_change_24h_new = df7['percent_change_24h'],
    percent_change_7d_new = df7['percent_change_7d'],
    percent_change_30d_new = df7['percent_change_30d'],
    percent_change_60d_new = df7['percent_change_60d'],
    percent_change_90d_new = df7['percent_change_90d']
)
df7['percent_change_24h_new'] = df7['percent_change_24h_new'].replace(['-', 'NaN'], np.nan)
df7['percent_change_7d_new'] = df7['percent_change_7d_new'].replace(['-', 'NaN'], np.nan)
df7['percent_change_30d_new'] = df7['percent_change_30d_new'].replace(['-', 'NaN'], np.nan)
df7['percent_change_60d_new'] = df7['percent_change_60d_new'].replace(['-', 'NaN'], np.nan)
df7['percent_change_90d_new'] = df7['percent_change_90d_new'].replace(['-', 'NaN'], np.nan)


# In[17]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[18]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[19]:


# Now to do something much simpler
# we are going to create a dataframe with the columns we want

df10 = df[['name','quote.USD.price','timestamp']]
df10 = df10.query("name == 'Bitcoin'")
df10


# In[20]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df10)


# In[ ]:





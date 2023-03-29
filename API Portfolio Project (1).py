#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com./v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '0d2e9da0-ae66-4078-840e-ea57c16cbf52',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[ ]:


import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[ ]:


df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[33]:


def api_runner():

    global df
    url = 'https://pro-api.coinmarketcap.com./v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '0d2e9da0-ae66-4078-840e-ea57c16cbf52',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df2 = pd.json_normalize(data['data'])
    df2['timestamp'] = pd.to_datetime('now')
    df
    
    if not os.path.isfile(r'C:\Users\owner\Documents\Python Scripts\API.csv'):
            df.to_csv(r'C:\Users\owner\Documents\Python Scripts\API.csv', header='column_names')
    else:
            df.to_csv(r'C:\Users\owner\Documents\Python Scripts\API.csv', mode='a', header=False)
    
    


# In[34]:


import os 
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API runner completed')
    sleep(60)
exit()


# In[35]:


df72 = pd.read_csv(r'C:\Users\owner\Documents\Python Scripts\API.csv')
df72


# In[36]:


pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[37]:


df


# In[41]:


df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()
df3


# In[42]:


df4 = df3.stack()
df4


# In[43]:


type(df4)


# In[44]:


df5 = df4.to_frame(name='values')
df5


# In[46]:


df5.count()


# In[51]:


index = pd.Index(range(90))

df6 = df5.reset_index()
df6


# In[54]:


df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[63]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h'],['1hr'])
df7


# In[64]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d'], ['24h', '7d', '30d', '60d', '90d'])
df7


# In[67]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[92]:


sns.catplot(x='percent_change', y ='values', hue='name', data=df7, kind='point')

plt.show()


# In[97]:


df8 = df[['name', 'quote.USD.price', 'timestamp']]
df8 = df8.query("name == 'Bitcoin'")
df8

df = df.loc[:,~df.columns.duplicated()]


# In[100]:


#df = df.reset_index()

#ignore_index=True

#df = df.loc[:,~df.columns.duplicated()]

sns.set_theme(style='darkgrid')

sns.lineplot(x='timestamp', y='quote.USD.price', data = df8)

plt.show()


# In[ ]:





# In[ ]:





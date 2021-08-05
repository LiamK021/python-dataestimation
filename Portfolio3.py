#!/usr/bin/env python
# coding: utf-8

# # Mobile Customer Churn
# 
# In this Portfolio task you will work with some (fake but realistic) data on Mobile Customer Churn with the goal of characterising customers who churn and building a simple predictive model to predict churn from available features. 
# 
# The data was generated (by Hume Winzar at Macquarie) based on a real dataset provided by Optus.  The data is simulated but the column headings are the same. (Note that I'm not sure if all of the real relationships in this data are preserved so you need to be cautious in interpreting the results of your analysis here).  
# 
# The data is provided in file `MobileCustomerChurn.csv` and column headings are defined in a file `MobileChurnDataDictionary.csv` (store these in the `files` folder in your project).
# 
# Your high level goal in this notebook are to:
# * look for significant clusters within the churn data - you might look separately at those who churn and those who don't or group them all together. 
# * try to build and evaluate a predictive model for churn - predict the value of the CHURN_IND field in the data from some of the other fields
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame
# In[3]:

###
churn = pd.read_csv("D:/CurrentTask/2021-5-27/Files/MobileCustomerChurn.csv")
churn.head()

df = DataFrame(churn,columns=['SERVICE_TENURE','AGE'])
  
kmeans = KMeans(n_clusters=4).fit(df)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(df['SERVICE_TENURE'],df['AGE'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=20)
plt.show()

###
df = DataFrame(churn, columns=['COUNTRY_METRO_REGION','CHURN_IND'])
plt.plot(df["CHURN_IND"],label='Close Price history')

deep_df = df.copy(deep = True)

numerical_columns = [col for col in df.columns if (df[col].dtype=='int64' or df[col].dtype=='float64') and col != 'Exited']

df[numerical_columns].describe().loc[['min','max', 'mean','50%'],:]

df[df['CHURN_IND'] == df['CHURN_IND'].min()]
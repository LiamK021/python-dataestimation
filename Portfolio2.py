#!/usr/bin/env python
# coding: utf-8

# # Sport Vouchers Program Analysis
# 
# The goal of this Portfolio task is to explore data from the Federal Government Sport Vouchers program - this is a
# program that provides up to two $100 vouchers for kids to participate in organised sport. Here's the [NSW Active Kids page](https://www.service.nsw.gov.au/transaction/apply-active-kids-voucher), there are similar schemes in other states. 
# 
# This is an exercise in exploring data and communicating the insights you can gain from it.  The source data comes
# from the `data.gov.au` website and provides details of all Sport Vouchers that have been redeemed since February 2015 as part of the Sport Voucher program:  [Sports Vouchers Data](https://data.gov.au/dataset/ds-sa-14daba50-04ff-46c6-8468-9fa593b9f100/details).  This download is provided for you as `sportsvouchersclaimed.csv`.
# 
# To augment this data you can also make use of [ABS SEIFA data by LGA](http://stat.data.abs.gov.au/Index.aspx?DataSetCode=ABS_SEIFA_LGA#) which shows a few measures of Socioeconomic Advantage and Disadvantage for every Local Government Area. This data is provided for you as `ABS_SEIFA_LGA.csv`. This could enable you to answer questions about whether the voucher program is used equally by parents in low, middle and high socioeconomic areas.   You might be interested in this if you were concerned that this kind of program might just benifit parents who are already advantaged (they might already be paying for sport so this program wouldn't be helping much).
# 
# Questions:
# * Describe the distribution of vouchers by: State, Sport - which states/sports stand out? 
# * Are some sports more popular in different states?
# * Are any electorates over/under represented in their use of vouchers? 
# * Is there a relationship between any of the SEIFA measures and voucher use in an LGA?

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame    
import math

# In[ ]:


# read the sports vouchers data
vouchers = pd.read_csv("D:/CurrentTask/2021-5-27/Files/sportsvouchersclaimed.csv")
vouchers.head()

from collections import Counter
sports = DataFrame(vouchers,columns=['Voucher_Sport'])
sportsArray = sports.to_numpy()

sports.mode()
clubs = DataFrame(vouchers, columns=['Club_Name'])
clubs.mode()
clubsArray = clubs.to_numpy()

####

newClubs = clubs.drop_duplicates(subset='Club_Name', keep="last")
newClubsArray = newClubs.to_numpy()

newSports = []

for index, newClub in enumerate(newClubsArray):
    selected = newClub
    clubSports = []
    for index1, club1 in enumerate(clubsArray):
        if  (selected == club1):
            #print(sportsArray[index1][0])
            clubSports.append(sportsArray[index1][0])
    newSports.append(clubSports)
   
for index, newClub in enumerate(newClubsArray):
    print(newClub[0] ,'=>' ,newSports[index][0])
    

###

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
completetionDate = DataFrame(vouchers, columns=['Voucher_Completion_Date']).to_numpy()
claimDate = DataFrame(vouchers, columns=['Voucher_Claim_Year']).to_numpy()
years =[]
for index, date in enumerate(completetionDate):
    try:
        date = date[0]
        year = date[5:7]
        #print(date, '=>', year, ':',RepresentsInt(year)  )
        years.append(int("20"+ year))
    except:
        years.append("0")

for index, year in enumerate(claimDate):
    claimed = year[0]
    print(years[index])
    try:
        if (years[index] >= claimed):
            print(index, '=> Over than', claimDate[index])
        if (years[index] < claimed):
            print(index, '=> Under than', claimDate[index])
    except:
        print(index, ': error here! check your db')

# The SEIFA data includes row for each Local Government Area (LGA) but the names of the LGAs have a letter or letters in brackets after the name.  To allow us to match this up with the voucher data we remove this and convert to uppercase. 
# 
# For each LGA the data includes a number of measures all of which could be useful in your exploration.  

# In[ ]:


# read the SEIFA data, create an LGA column by removing the letters in brackets and converting to uppercase
seifa = pd.read_csv('D:/CurrentTask/2021-5-27/Files/ABS_SEIFA_LGA.csv')
lga = seifa["Local Government Areas - 2011"].str.replace(' \([ACSRCDMT]+\)', '').str.upper()
seifa['LGA'] = lga
seifa.head()


# Since there are many rows per LGA we need to use `pivot_table` to create a new data frame with one row per LGA. Here
# is an example of doing this to create a table with the different SCORE measures and the population (URP) field. 

# In[ ]:


LGA_scores = seifa[seifa.MEASURE == 'SCORE'].pivot_table(index="LGA", columns=["INDEX_TYPE"], values="Value")
LGA_scores.head()
LGA_pop = seifa[seifa.MEASURE == 'URP'].pivot_table(index="LGA", columns=["INDEX_TYPE"], values="Value")
LGA_scores['Population'] = LGA_pop.IEO
LGA_scores.head()

print(LGA_scores)

# This data frame can then be joined with the vouchers data fram to create one master data frame containing both the voucher data and the SEIFA measures.

# In[ ]:


vouchers_scores = vouchers.join(LGA_scores, on='Participant_LGA')
vouchers_scores.head()


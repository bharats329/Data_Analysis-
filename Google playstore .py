#!/usr/bin/env python
# coding: utf-8

# In[2]:


#importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


# ## Reading data from the CSV file

# In[3]:


data=pd.read_csv("D:/W.O.R.K/Python/googleplaystore_dataset/googleplaystore.csv")
data.head()


# In[4]:


data.columns = data.columns.str.replace(' ', '_')


# In[5]:


print("shape of Data: ",data.shape)
print("data types: \n", data.dtypes.value_counts())


# ## SIZE
# 

# In[6]:


data.Size.value_counts().head()


# In[8]:


#replacing k and M with their values to convert values to numeric.
data.Size=data.Size.str.replace('k','e+3')
data.Size=data.Size.str.replace('M','e+6')
data.Size.head()


# Now, we have some two types of values in our Size data.
# 
# exponential values (not yet converted to string)
# Strings (that cannot be converted into numeric)
# Thus specifing categories 1 and 2 as an boolean array temp, to convert category 1 to numeric.

# In[9]:


def is_convertable(v):
    try:
        float(v)
        return True
    except ValueError:
        return False
    
temp=data.Size.apply(lambda x: is_convertable(x))
temp.head()


# Now checking unique non numeric values(~temp) in Size.

# In[12]:


data.Size[~temp].value_counts()


# Replacing 'Varies with Device' by nan and
# converting 1,000+ to 1000, to make it numeric

# In[13]:


data.Size=data.Size.replace('Varies with device', np.nan)
data.Size=data.Size.replace('1,000+', 1000)


# Converting the cleaned Size data to numeric type

# In[14]:


data.Size=pd.to_numeric(data.Size)


# ## INSTALLS

# Checking unique values in install data 

# In[16]:


data.Installs.value_counts()


# It can be seen that there are 22 unique values, out of which 

# 1 is 0
# 

# 1 is Free(string), which we will be converting to nan here

# And rest are numeric but with '+' and ','which shall be removed to convert these into numeric type.

# In[18]:


data.Installs=data.Installs.apply(lambda x: x.strip('+'))
data.Installs=data.Installs.apply(lambda x: x.replace(',',''))
data.Installs=data.Installs.replace('Free',np.nan)
data.Installs.value_counts()


# Checking if data is converted to numeric

# In[19]:


data.Installs.str.isnumeric().sum()


# Now in Installs only 1 sample is non numeric out of 10841, which is nan ("Free")

# In[20]:


data.Installs=pd.to_numeric(data.Installs)


# ## REVIEWS

# Checking if all values in number of Reviews numeric

# In[21]:


data.Reviews.str.isnumeric().sum()


# One review is non numeric out of 10841.

# In[22]:


data[~data.Reviews.str.isnumeric()]


# The entries in this row are enrterd wrong way. So let's delete this row for now .

# In[23]:


data=data.drop(data.index[10472])


# Let's check if the row is deleted

# In[25]:


data[10472: ].head(2)


# In[26]:


data.Reviews=data.Reviews.replace(data.Reviews[~data.Reviews.str.isnumeric()],np.nan)


# ## RATING

# For entries to be right we need to make sure they fall within the range 1 to 5 

# In[27]:


print("Range:", data.Rating.min(),"-", data.Rating.max())


# Checking the type of data, to see if it needs to be converted to numeric

# In[28]:


data.Rating.dtype


# Data is already in numeric value now let's check for any null values

# In[29]:


print(data.Rating.isna().sum(), "null values out of ",len(data.Rating))


# ## TYPE

# Checking for unique type values and any problem with the data

# In[30]:


data.Type.value_counts()


# There are only two types, free and paid. No unwanted data here.

# ## Price

# Checking for unique values of price, along with any abnormalities

# In[32]:


data.Price.unique()


# Data had $ sign which shall be removed to convert it to numeric

# In[34]:


data.Price=data.Price.apply(lambda x: x.strip('$'))


# In[35]:


data.Price=pd.to_numeric(data.Price)


# ## CATEGORY

# Now let's inspect the category by looking into the unique terms

# In[36]:


data.Category.unique()


# In[37]:


data.Category.value_counts().plot(kind='bar')


# ## CONTENT RATING

# Checking unique terms in Content Rating Categories, and for repetitve or abnormal data

# In[38]:


data.Content_Rating.unique()


# No abnormalies or repetiton found

# In[40]:


data.Content_Rating.value_counts().plot(kind='bar')
plt.yscale('log')


# ## GENRES

# Checking for unique values, abnormalitity or repetition in data

# In[41]:


data.Genres.unique()


# The data is in the format Category;Subcategory. Let's divide the data into two columns, one as primary category and the other as secondary,  using ; as separator

# In[42]:


sep=';'
rest = data.Genres.apply(lambda x: x.split(sep)[0])
data['Pri_Genres']=rest
data.Pri_Genres.head()


# In[45]:


rest = data.Genres.apply(lambda x: x.split(sep)[-1])
rest.unique()
data['Sec_Genres']=rest
data.Sec_Genres.head()


# In[47]:


grouped = data.groupby(['Pri_Genres','Sec_Genres'])
grouped.size().head(15)


# Generating a two table to better understand the relationship between primary and secondary categories of Genres

# In[48]:


twowaytable = pd.crosstab(index=data["Pri_Genres"], columns=data["Sec_Genres"])
twowaytable.head()


# ## LAST UPDATED

# Checking the format of data in Last Updated Dates

# In[49]:


data.Last_Updated.head()


# Converting the data i.e. string to datetime format for further processing

# In[50]:


from datetime import datetime,date
temp=pd.to_datetime(data.Last_Updated)
temp.head()


# Taking a difference between last updated date and today tio simplify the data for future processing. It gives days.

# In[51]:


data['Last_Updated_Days'] = temp.apply(lambda x:date.today()-datetime.date(x))
data.Last_Updated_Days.head()


# ## ANDROID VERSION

# Checking unique values, repetition, or any abnormalities.

# In[52]:


data.Android_Ver.unique()


# Most of the values have a upper value and a lower value (i.e. a range), lets divide them as two new features Version begin and end, which might come handy while procesing data further.

# In[55]:


data['Version_begin']=data.Android_Ver.apply(lambda x:str(x).split(' and ')[0].split('-')[0])
data.Version_begin=data.Version_begin.replace('4.4W','4.4')
data['Version_end']=data.Android_Ver.apply(lambda x:str(x).split(' and ')[-1].split(' - ')[-1])


# In[56]:


data.Version_begin.unique()


# Representing categorial data as two way table and plotting it as stacked columns for better understanding

# In[57]:


twowaytable = pd.crosstab(index=data.Version_begin, columns=data.Version_end)
twowaytable.head()


# In[58]:


data.Version_end.unique()


# ## CURRENT VERSION

# In[59]:


data.Current_Ver.value_counts().head(6)


# Lets convert all the version in the format number.number to simplify the data, and check if the data has null values. Also, we are not considering converting value_counts to nan here due to its high frequency.

# In[60]:


data.Current_Ver.isna().sum()


# As we have only 8 nans lets replace them with Varies with data to simplify

# In[62]:


import re
temp=data.Current_Ver.replace(np.nan,'Varies with device')
temp=temp.apply(lambda x: 'Varies with device' if x=='Varies with device' else re.findall('^[0-9]\.[0-9]|[\d]|\W*',str(x))[0])


# In[64]:


temp.unique()


# Saving the updated current version values as a new column

# In[65]:


data['Current_Ver_updated']=temp


# In[67]:


data.Current_Ver_updated.value_counts().plot(kind="barh", figsize=(15,15));
plt.legend(bbox_to_anchor=(1.0,1.0))
plt.xscale('log')


# In[68]:


data.head()


# In[69]:


data.to_csv('Updated_googleplaystore_dataset.csv')


# In[ ]:





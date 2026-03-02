#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Importing libraries for data manipulation

import pandas as pd

import numpy as np

# Importing libraries for data visualization

import seaborn as sns

import matplotlib.pyplot as plt

# Importing libraries for builind linear regression model

import statsmodels.api as sm

from statsmodels.stats.outliers_influence import variance_inflation_factor

# Importing libraries for scaling the data

from sklearn.preprocessing import MinMaxScaler

# To ignore warnings

import warnings

warnings.filterwarnings("ignore")



df = pd.read_excel(r"C:\Users\andre\Documents\Doc_Andrea\Data Science\Projects (external sources)\weatherHistory.xlsx")

df


# In[2]:


df.isnull()


# In[3]:


null_count = df.isnull().sum().sum()
print('Number of null values:', null_count)


# In[6]:


df.dropna(subset = ['Precip Type', 'Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 
                    'Wind Bearing (degrees)', 'Visibility (km)', 'Loud Cover', 'Pressure (millibars)', 'Daily Summary'])


# In[7]:


df.dropna(how='all')


# In[8]:


df.dropna(axis='columns')


# In[15]:


train_df = df.drop(['Formatted Date', 'Summary', 'Loud Cover', 'Daily Summary'], axis = 1)


# In[16]:


train_df


# In[21]:


temp_hum_df = df.drop(['Formatted Date', 'Precip Type', 'Wind Speed (km/h)', 'Wind Bearing (degrees)', 'Visibility (km)', 'Pressure (millibars)', 'Summary', 'Loud Cover', 'Daily Summary'], axis = 1)


# In[22]:


temp_hum_df


# In[24]:


train_df.info()


# In[25]:


temp_hum_df.info() 


# In[51]:


# Univariate analysis: analyzing/visualizing the dataset by taking one variable at a time
# Let's start with analyzing the categorical variables present in the data corresponding to train_df.
# There is one categorical variable in this dataset and we will create univariate bar charts for it to check their distribution.

fig = plt.figure(figsize = (18, 6))

fig.suptitle('Barplot for the categorical variable in the modified dataset')

sns.countplot(x = 'Precip Type', data = train_df, color = 'paleturquoise', order = train_df['Precip Type'].value_counts().index);


# In[66]:


# Univariate analysis: analyzing/visualizing the dataset by taking one variable at a time
# Let's start with analyzing the categorical variables present in the data corresponding to the original dataset.
# There are 4 variable in this dataset and we will create univariate bar charts for it to check their distribution.

fig, axes = plt.subplots (4, 1, figsize = (14, 18))

fig.suptitle('Bar plot for the categorical variables in the original dataset')

sns.countplot(ax = axes [0], x = 'Summary', data = df, color = 'darkturquoise', order = df['Summary'].value_counts().index[:10]);

sns.countplot(ax = axes [1], x = 'Daily Summary', data = df, color = 'darkturquoise', order = df['Daily Summary'].value_counts().index[:10]);

sns.countplot(ax = axes [2], x = 'Precip Type', data = df, color = 'darkturquoise', order = df['Precip Type'].value_counts().index);

sns.countplot(ax = axes [3], x = 'Loud Cover', data = df, color = 'darkturquoise', order = df['Loud Cover'].value_counts().index);

plt.xticks(rotation = 45);

for ax in axes.flatten():
    for label in ax.get_xticklabels():
        label.set_rotation(45)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


# In[68]:


import matplotlib.pyplot as plt
import seaborn as sns

# List of categorical columns you want to plot

categorical_vars = ['Summary', 'Daily Summary', 'Precip Type', 'Loud Cover']

# Calculate number of subplots and adjust figure height accordingly
num_subplots = len(categorical_vars)

# Dynamically calculate height based on max number of categories
max_cats = max([df[col].nunique() for col in categorical_vars])
height_per_cat = 0.5 # adjust this number to control vertical spacing
fig_height = max(num_subplots * height_per_cat * max_cats, 8) # minimum height of 8

# Create subplots
fig, axes =plt.subplots(num_subplots, 1, figsize = (14, fig_height))
fig.suptitle('Barplot for the categorical variables in the original dataset', fontsize = 16)

# Plot each categorical variable
for i, col in enumerate(categorical_vars):
    sns.countplot (ax = axes[i], x = col, data = df, color = 'darkturquoise',
                  order = df[col].value_counts().index[:10]) # Limit to top 10 if needed
    axes[i].set_title(col)
    axes[i].tick_params(axis = 'x', rotations = 45)
    
# Adjust layout
plt.tight_layout(rect = [0, 0.03, 1, 0.95])
plt.show()


# In[48]:


# Below we are analyzing all the numerical variables present in the data. 
# Since we want to visualize one numerical variable at a time, histogram is the best choice to visualize the data.

fig, axes = plt.subplots (4, 2, figsize = (20, 17))

fig.suptitle('Histogram for all numerical variables in the dataset')

sns.histplot(x = "Temperature (C)", data = train_df, kde = True, ax = axes[0, 0]);

sns.histplot(x = "Apparent Temperature (C)", data = train_df, kde = True, ax = axes[0, 1]);

sns.histplot(x = "Humidity", data = train_df, kde = True, ax = axes[1, 0]);

sns.histplot(x = "Wind Speed (km/h)", data = train_df, kde = True, ax = axes[1, 1]);

sns.histplot(x = "Wind Bearing (degrees)", data = train_df, kde = True, ax = axes[2, 0]);

sns.histplot(x = "Visibility (km)", data = train_df, kde = True, ax = axes[2, 1]);

sns.histplot(x = "Pressure (millibars)", data = train_df, kde = True, ax = axes[3, 0]);

# Remove the empty plot

fig.delaxes(axes[3,1]) 


# In[ ]:





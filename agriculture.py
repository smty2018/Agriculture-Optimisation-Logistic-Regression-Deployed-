# -*- coding: utf-8 -*-
"""agriculture.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MooxCkjPagWzBmg88xzRkavqRiIV2bIe

###Import Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets
from ipywidgets import interact
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

data=pd.read_excel("data.xlsx")

data.describe()

data["label"].value_counts()

data.shape

data.head()

data.isnull().sum()

"""#Analytics"""

data['N'].mean()

data['P'].mean()

data['K'].mean()

data['ph'].mean()

data['rainfall'].mean()

data['humidity'].mean()

data['temperature'].mean()

@interact
def summary(crops = list(data['label'].value_counts().index)):
    x = data[data['label'] == crops]
    print("---------------------------------------------")
    print("Nitrogen")
    print(" Min Nitrigen   :", x['N'].min())
    print("Avg Nitrogen   :", x['N'].mean())
    print("Max Nitrogen   :", x['N'].max())
    print("---------------------------------------------")
    print("Phosphorous")
    print(" Min Phosphorous   :", x['P'].min())
    print("Avg Phosphorous   :", x['P'].mean())
    print("Max Phosphorous   :", x['P'].max())
    print("---------------------------------------------")
    print("Potassium")
    print(" Min Potassium :", x['K'].min())
    print("Avg Potassium :", x['K'].mean())
    print("Max Potassium :", x['K'].max())
    print("---------------------------------------------")
    print("Temperature")
    print(" Min Temp : {}".format(x['temperature'].min()))
    print("Avg Temp : {}".format(x['temperature'].mean()))
    print("Max Temp : {}".format(x['temperature'].max()))
    print("---------------------------------------------")
    print("Statistics for Humidity")
    print(" Min Humidity   : {}".format(x['humidity'].min()))
    print("Avg Humidity   : {}".format(x['humidity'].mean()))
    print("Max Humidity   : {}".format(x['humidity'].max()))
    print("---------------------------------------------")
    print("PH")
    print(" Min PH   : {0:.2f}".format(x['ph'].min()))
    print("Avg PH   : {0:.2f}".format(x['ph'].mean()))
    print("Max PH   : {0:.2f}".format(x['ph'].max()))
    print("---------------------------------------------")
    print("Rainfall")
    print(" Min Rainfall   : {0:.2f}".format(x['rainfall'].min()))
    print("Avg Rainfall   : {0:.2f}".format(x['rainfall'].mean()))
    print("Max Rainfall   : {0:.2f}".format(x['rainfall'].max()))

@interact
def compare(conditions=["N","P","K","temperature","ph","humidity","rainfall"]):
  print("Low Sustainable Crops\n")
  print(data[data[conditions]> data[conditions].mean()]['label'].unique())

@interact
def compare(conditions=["N","P","K","temperature","ph","humidity","rainfall"]):
  print("High Sustainable Crops\n")
  print(data[data[conditions]< data[conditions].mean()]['label'].unique())

plt.subplot(1,1,1)
sns.histplot(data['N'],color="blue")
plt.title("Nitrogen")
plt.grid()
plt.show()

plt.subplot(1,1,1)
sns.histplot(data['P'],color="red")
plt.title("Phosphorus")
plt.grid()
plt.show()

plt.subplot(1,1,1)
sns.histplot(data['K'],color="yellow")
plt.title("Potassium")
plt.grid()
plt.show()

plt.subplot(1,1,1)
sns.histplot(data['temperature'],color="orange")
plt.title("Temperature(C)")
plt.grid()
plt.show()

plt.subplot(1,1,1)
sns.histplot(data['ph'],color="pink")
plt.title("ph")
plt.grid()
plt.show()

plt.subplot(1,1,1)
sns.histplot(data['humidity'],color="green")
plt.title("Humidity")
plt.grid()
plt.show()

plt.subplot(1,1,1)
sns.histplot(data['rainfall'],color="black")
plt.title("Rainfall(mm)")
plt.grid()
plt.show()

print("Summer Crops")
print(data[(data['temperature'] > 30) & (data['humidity'] > 50)]['label'].unique())

print("Winter Crops")
print(data[(data['temperature'] < 20) & (data['humidity'] > 30)]['label'].unique())

print("Rainy Crops")
print(data[(data['rainfall'] > 200) & (data['humidity'] > 30)]['label'].unique())

"""###Clustering with KMeans"""

x=data.loc[:,["N","P","K","temperature","ph","humidity","rainfall"]]
x_data=pd.DataFrame(x)

x_data.head()

plt.rcParams["figure.figsize"]=(10,4)
l=[]
for i in range(1,11):
  k=KMeans(n_clusters=i,init="k-means++",max_iter=500,n_init=10,random_state=0)
  k.fit(x)
  l.append(k.inertia_)
  print(l)

plt.plot(range(1,11),l)
plt.show

k = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
y_means = k.fit_predict(x)

a = data['label']
y_means = pd.DataFrame(y_means)
z = pd.concat([y_means, a], axis = 1)
z = z.rename(columns = {0: 'cluster'})

counts = z[z['cluster'] == 0]['label'].value_counts()
d = z.loc[z['label'].isin(counts.index[counts >= 50])]
d = d['label'].value_counts()
print("Cluster 1:", list(d.index))

counts = z[z['cluster'] == 1]['label'].value_counts()
d = z.loc[z['label'].isin(counts.index[counts >= 50])]
d = d['label'].value_counts()
print("Cluster 2:", list(d.index))

counts = z[z['cluster'] == 2]['label'].value_counts()
d = z.loc[z['label'].isin(counts.index[counts >= 50])]
d = d['label'].value_counts()
print("Cluster 3:", list(d.index))

counts = z[z['cluster'] == 3]['label'].value_counts()
d = z.loc[z['label'].isin(counts.index[counts >= 50])]
d = d['label'].value_counts()
print("Cluster 4:", list(d.index))

"""###Logistic Regression"""

y=data['label']
x=data.drop(["label"],axis=1)
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)

lr=LogisticRegression()
lr.fit(x_train,y_train)
y_pred=lr.predict(x_test)

cr = classification_report(y_test, y_pred)
print(cr)
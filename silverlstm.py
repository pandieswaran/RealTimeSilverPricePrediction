# -*- coding: utf-8 -*-
"""SilverLSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17oz7GxN0ykd-zAVzsURMLM7Q3_G45Drh
"""

#For getting a Realtime Data From the Yahoo Finance 
!pip install yfinance

#To get a Data from Website using YFinance Library
import yfinance as yf

msft = yf.Ticker("SI=F")

# get the historical market data Specific Date
hist = msft.history(start="2020-01-01", end="2023-12-31")

import pandas as pd

#To get a CSV File 
hist.to_csv('Silver.csv')

hist.head()

df1 = hist.reset_index()['Close']

df1.shape

import matplotlib.pyplot as plt

plt.plot(df1)

#LSTM are sensitive to the scale of the data. So we apply MinMaxSCaler

import numpy as np

from sklearn.preprocessing import MinMaxScaler

Scaler = MinMaxScaler(feature_range=(0,1))

df1 = Scaler.fit_transform(np.array(df1).reshape(-1,1))

#Splitting Dataset into Train and Test Split

Training_Size = int(len(df1)*0.80)
Test_Size = len(df1) - Training_Size
Train_data , Test_data = df1[0:Training_Size,:] , df1[Training_Size:len(df1),:1]

Training_Size , Test_Size

#Converting An Array Of Value into A Dataset Matrix
import numpy
def create_dataset(dataset, time_step = 1):
    dataX , dataY = [] , []
    for i in range(len(dataset)-time_step-1):
      a = dataset[i:(i+time_step), 0 ]
      dataX.append(a)
      dataY.append(dataset[i + time_step,0])
    return numpy.array(dataX) , numpy.array(dataY)

#reshape into X=t t+1 t+2 t+3 t+4 and y=t+5
time_step=100
X_Train , Y_Train = create_dataset(Train_data,time_step)
X_Test , Y_Test = create_dataset(Test_data,time_step)

#Print the 4 timeStep Features Array Value
print(X_Train)

print(X_Train.shape) , print(Y_Train.shape)

print(X_Test.shape) , print(Y_Test.shape)

#reshape input to  be [Sample , TimeStep ,Features] Which is required for LSTM 
X_Train = X_Train.reshape(X_Train.shape[0],X_Train.shape[1],1)
X_Test = X_Test.reshape(X_Test.shape[0],X_Test.shape[1],1)

#Create a The Stacked LSTM Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

model = Sequential()
model.add(LSTM(50,return_sequences = True , input_shape = (100,1)))
model.add(LSTM(50,return_sequences = True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error' , optimizer = 'adam')

model.summary()

model.fit(X_Train,Y_Train,validation_data=(X_Test,Y_Test), epochs=100,batch_size=64,verbose=1)

import tensorflow as tf

#let do the prediction and check the performance metrics
Train_Predict = model.predict(X_Train)
Test_Predict = model.predict(X_Test)

#Transform to original form
Train_Predict = Scaler.inverse_transform(Train_Predict)
Test_Predict = Scaler.inverse_transform(Test_Predict)

#Calculate RMSE Performance Metric
import math 
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(Y_Train,Train_Predict))

#Test Data RMSE
math.sqrt(mean_squared_error(Y_Test,Test_Predict))

#Plotting

#shift train predictions for plotting

look_back=100

trainPredictPlot = numpy.empty_like(df1)

trainPredictPlot[:, :] = np.nan # plot baseline and predictions

trainPredictPlot[look_back: len(Train_Predict)+look_back, ] = Train_Predict

#shift test predictions for plotting

testPredictPlot = numpy.empty_like(df1)
testPredictPlot[:, :]= numpy.nan
testPredictPlot [len(Train_Predict)+(look_back*2)+1:len (df1)-1,] = Test_Predict

plt.plot(Scaler.inverse_transform(df1))

plt.plot(trainPredictPlot)

plt.plot(testPredictPlot)

plt.show()
#Orange is Train Predict Data
#Green is Test Predict Data

len(Test_data)

X_Input = Test_data[58:].reshape(1,-1)

X_Input.shape

temp_input = list(X_Input)
temp_input = temp_input[0].tolist()

lst_output=[]

n_steps=100 
i = 0

while (i < 30) :

  if(len(temp_input)>100):

    #print(temp_input)

    x_input=np.array(temp_input[1:])

    print("{} day input {}".format(i,x_input))

    x_input=x_input.reshape(1,-1)

    x_input = x_input.reshape((1, n_steps, 1)) 

    #print(x_input)

    yhat = model.predict(x_input, verbose=0)

    print("{} day output {}".format(i,yhat))

    temp_input.extend(yhat[0].tolist())

    temp_input=temp_input[1:]

    #print(temp_input)

    lst_output.extend(yhat.tolist())
    i = i + 1
  else:
    X_Input = X_Input.reshape((1, n_steps,1)) 
    yhat = model.predict(X_Input, verbose=0) 
    print(yhat[0]) 
    temp_input.extend(yhat[0].tolist()) 
    print(len(temp_input))
    lst_output.extend(yhat.tolist())
    i = i + 1

print(lst_output)

Day_New = np.arange(1,101)
Day_Pred = np.arange(101,131)

import matplotlib.pyplot as plt

len(df1)

df3 = df1.tolist()
df3.extend(lst_output)

plt.plot(Day_New,Scaler.inverse_transform(df1[688:]))
plt.plot(Day_Pred,Scaler.inverse_transform(lst_output))
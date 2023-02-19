import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import load_model
from tensorflow import keras

import streamlit as st

from get_temp_csv import get_temp_csv
from plots import *
from calc_TI import *

st.set_option('deprecation.showPyplotGlobalUse', False)


st.title("EZ_money @ Maze Bank")

ticker = st.text_input('Enter Stock Ticker ', 'AAPL')


# using get_temp_csv tgo make a temp csv to get data and etc
# get_temp_csv(ticker)
df = pd.read_csv(get_temp_csv(ticker))
df = ema_n(df, 100)
df = ema_n(df, 200)
df = vwap(df)
df = get_trend(df)

st.subheader('check')
st.pyplot(plot_chart(df[:100]))

st.subheader('check')
st.write(df.head())

df = df.drop(['time', 'open', 'high', 'low', 'volume'], axis=1)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

x0=[]
x1=[]
x2=[]
x3=[]
y=[]
for i in range (0, df.shape[0] - 200):
    x0.append(df.iloc[i:i+200, 0])
    x1.append(df.iloc[i:i+200, 1])
    x2.append(df.iloc[i:i+200, 2])
    x3.append(df.iloc[i:i+200, 3])
    y.append(df.iloc[i+200, 4])

x0, x1, x2, x3, y= np.array(x0), np.array(x1), np.array(x2), np.array(x3), np.array(y)

x0 = scaler.fit_transform(x0)
x1 = scaler.fit_transform(x1)
x2 = scaler.fit_transform(x2)
x3 = scaler.fit_transform(x3)

X = np.stack([x0, x1, x2, x3], axis=2)

model = load_model('..\\models\\bot\\bot-multi-1.hdf5')

predictions = model.predict(X)

st.subheader('check')
st.pyplot(plot_res(predictions, y))
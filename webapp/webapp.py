import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import json

from keras.models import load_model
from tensorflow import keras
from datetime import datetime

import streamlit as st

from get_temp_csv import *
from technical_indicators import *  
from get_chart import *

import pandas_ta as ta
from ta.volume import VolumeWeightedAveragePrice
# -----------------------------------------------------------

try:
    st.set_page_config(layout="wide")
except:
    st.beta_set_page_config(layout="wide")


# -----------------------------------------------------------

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Stock Trend Prediction")

ticker = st.text_input('Enter Stock Ticker ', 'AAPL')


overview_data = get_overview(ticker)

st.write(overview_data["Name"])
st.write(overview_data["Description"])

# using get_temp_csv tgo make a temp csv to get data and etc
# get_temp_csv(ticker)
df = pd.read_csv(get_temp_csv(ticker))

# -----------------------------------------------------------
# chart

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(get_candlestick_chart(ticker, df))

# -------------------------------------------------------
# Getting EMA and EMA Signal
wb_ema_n(df, 100)
wb_ema_n(df, 200)
wb_ema_signal(df)

# VWAP
wb_vwap(df)
generate_signal_vwap(df)

# StochasticRSI
wb_stochrsi(df)

# MACD 
wb_macd(df)
df['macd_signal'] = df['macd_signal'].astype(int)

# Price_ABS_PCT
get_abs_pct(df)

# Trend
get_trend(df)

# cleaning df
df = df.dropna()
df.reset_index(inplace=True)
df = df.drop('index',axis=1)


df.to_csv('test.csv')

# ----------------------------------------------------------
# scaling and reindexing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

df[[
    'open', 'high', 'low', 'close', 'volume', 'ema_100', 'ema_200', 'vwap', 'STOCHk_14_3_3', 'STOCHd_14_3_3', 
    'MACD_12_26_9',	'MACDs_12_26_9', 'MACDh_12_26_9', 'volume_change', 'volume_pct_change', 
    'open_change', 'high_change', 'low_change', 'close_change', 'open_pct_change', 'high_pct_change', 
    'low_pct_change', 'close_pct_change'
    ]] = scaler.fit_transform(df[[
                                    'open', 'high', 'low', 'close', 'volume', 'ema_100', 'ema_200', 'vwap', 'STOCHk_14_3_3',
                                    'STOCHd_14_3_3', 'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9', 'volume_change', 'volume_pct_change',
                                    'open_change', 'high_change', 'low_change', 'close_change', 'open_pct_change', 'high_pct_change', 
                                    'low_pct_change', 'close_pct_change']])

df = df.reindex(columns=[ 'open', 'open_change', 'open_pct_change', 'high', 'high_change', 'high_pct_change', 'low', 'low_change',  'low_pct_change',
                        'close', 'close_change', 'close_pct_change', 'volume', 'volume_change', 'volume_pct_change', 
                        'ema_100', 'ema_200', 'vwap', 'STOCHk_14_3_3', 'STOCHd_14_3_3', 
                        'MACD_12_26_9',	'MACDs_12_26_9', 'MACDh_12_26_9', 
                        'ema_signal', 'vwap_signal', 'stochrsi_signal', 'macd_signal', 'trend'
    ])

# st.subheader('Preprocessing the dataframe')
# st.write('Below is the normalized dataframe which is fed to to the model to give out predictions ')
# st.write(df.describe())

# --------------------------------------------------------------
# making np array stacks to fit data into lstm dim
# n col, 230 timesteps, 28 features
o0 = []
o1 = []
o2 = []
h0 = []
h1 = []
h2 = []
l0 = []
l1 = []
l2 = []
c0 = []
c1 = []
c2 = []
v0 = []
v1 = []
v2 = []
em1 = []
em2 = []
vw = []
stk= []
std = []
ma = []
ms = []
mh = []
em_s = []
vw_s = []
st_s = []
ma_s = []

y = []

for i in range (0, df.shape[0] - 230):
    o0.append(df.iloc[i:i+230, 0])
    o1.append(df.iloc[i:i+230, 1])
    o2.append(df.iloc[i:i+230, 2])
    h0.append(df.iloc[i:i+230, 3])
    h1.append(df.iloc[i:i+230, 4])
    h2.append(df.iloc[i:i+230, 5])
    l0.append(df.iloc[i:i+230, 6])
    l1.append(df.iloc[i:i+230, 7])
    l2.append(df.iloc[i:i+230, 8])
    c0.append(df.iloc[i:i+230, 9])
    c1.append(df.iloc[i:i+230, 10])
    c2.append(df.iloc[i:i+230, 11])
    v0.append(df.iloc[i:i+230, 12])
    v1.append(df.iloc[i:i+230, 13])
    v2.append(df.iloc[i:i+230, 14])
    em1.append(df.iloc[i:i+230, 15])
    em2.append(df.iloc[i:i+230, 16])
    vw.append(df.iloc[i:i+230, 17])
    stk.append(df.iloc[i:i+230, 18])
    std.append(df.iloc[i:i+230, 19])
    ma.append(df.iloc[i:i+230, 20])
    ms.append(df.iloc[i:i+230, 21])
    mh.append(df.iloc[i:i+230, 22])
    em_s.append(df.iloc[i:i+230, 23])
    vw_s.append(df.iloc[i:i+230, 24])
    st_s.append(df.iloc[i:i+230, 25])
    ma_s.append(df.iloc[i:i+230, 26])

    y.append(df.iloc[i+230, 27])

# ---------------------------------------------------------

o0, o1, o2, h0, h1, h2, l0, l1, l2, c0, c1, c2, v0, v1, v2, em1, em2, vw, stk, std, ma ,ms, mh, em_s, vw_s, st_s, ma_s, y = np.array(o0), np.array(o1), np.array(o2), np.array(h0), np.array(h1), np.array(h2), np.array(l0), np.array(l1), np.array(l2), np.array(c0), np.array(c1), np.array(c2), np.array(v0), np.array(v1), np.array(v2), np.array(em1), np.array(em2), np.array(vw), np.array(stk), np.array(std), np.array(ma), np.array(ms), np.array(mh), np.array(em_s), np.array(vw_s), np.array(st_s), np.array(ma_s), np.array(y)

y=np.reshape(y, (len(y), 1))

X = np.stack([o0, o1, o2, h0, h1, h2, l0, l1, l2, c0, c1, c2, v0, v1, v2, em1, em2, vw, stk, std, ma ,ms, mh, em_s, vw_s, st_s, ma_s], axis=2)

model = load_model('..\\dmn\\main-relu-(128, 128, 128)-sgd-period7.hdf5')

predictions = model.predict(X)

cmp =[1 if x > 0.25 else -1 if x < -0.25 else 0 for x in predictions]
real = [item for sublist in y for item in sublist]

curr_pred = predictions[-1]

with col2:
    st.subheader("\tCurrent Prediction")
    if curr_pred > 0.25:
        pct = (curr_pred * 100)
        pctc = 100 if pct > 100.00 else pct
        st.write(f"\tBuy with confidence % {pctc}")

    elif curr_pred < -0.25:
        pct = (-(curr_pred * 100))
        pctc =  100 if pct > 100.00 else pct
        st.write(f"\tSell with confidence % {pctc}")

    st.write("")
    st.write("")

st.subheader("Real vs Predicted graph ")
st.plotly_chart(get_pred_chart(real, cmp))
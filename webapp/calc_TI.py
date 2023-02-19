import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ta.volume import VolumeWeightedAveragePrice


def calculate_ema(data, n):
    ema = data.close.ewm(span=n, adjust=False).mean()
    return ema

def ema_n(raw_df, n):
    close_price = raw_df['close']
    ema_n = calculate_ema(raw_df, n)
    ema_n = ema_n.round(3)
    raw_df['EMA_{}'.format(n)] = ema_n
    return raw_df

def vwap(raw_df, label='VWAP', window=3, fillna=True):
        vwap_hcl3 = VolumeWeightedAveragePrice(high=raw_df['high'], low=raw_df['low'], close=raw_df["close"], volume=raw_df['volume'], window=window, fillna=fillna).volume_weighted_average_price()
        vwap_hcl3 = vwap_hcl3.round(3)
        raw_df[label] = vwap_hcl3
        return raw_df

def get_trend(raw_df):
    raw_df['trend'] = [1 if (row['close'] > row['EMA_200'] + 0.00125 * row['close']) and (row['close'] > row['EMA_100'] + 0.001 * row['close']) and (row['close'] > row['VWAP'] + 0.0005 * row['close'])
                        else -1 if row['close'] < row['EMA_200'] - 0.00125 * row['close'] and (row['close'] < row['EMA_100'] + 0.001 * row['close']) and (row['close'] < row['VWAP'] + 0.0005 * row['close'])
                        else 0 
                        for index, row in raw_df.iterrows()]
    return raw_df
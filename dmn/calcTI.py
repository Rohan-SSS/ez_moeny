import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ta.volume import VolumeWeightedAveragePrice


def calculate_ema(data, n):
    ema = data.Close.ewm(span=n, adjust=False).mean()
    return ema

def ema_n(raw_df, n):
    close_price = raw_df['Close']
    ema_n = calculate_ema(raw_df, n)
    ema_n = ema_n.round(3)
    raw_df['EMA_{}'.format(n)] = ema_n
    return raw_df

def vwap(raw_df, label='VWAP', window=3, fillna=True):
        vwap_hcl3 = VolumeWeightedAveragePrice(high=raw_df['High'], low=raw_df['Low'], close=raw_df["Close"], volume=raw_df['Volume'], window=window, fillna=fillna).volume_weighted_average_price()
        vwap_hcl3 = vwap_hcl3.round(3)
        raw_df[label] = vwap_hcl3
        return raw_df
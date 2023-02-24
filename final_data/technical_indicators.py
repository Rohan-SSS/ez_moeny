import numpy as np
import pandas as pd
import pandas_ta as ta
from ta.volume import VolumeWeightedAveragePrice

def calculate_ema(data, n):
    ema = data.close.ewm(span=n, adjust=False).mean()
    return ema

def generate_signals_vwap(df):
    sell_signal = df['close'] < (df['vwap'] + (0.001 * df['close']))
    buy_signal = df['close'] > (df['vwap'] + (0.001 * df['close']))
    return buy_signal, sell_signal

def generate_signals_rsi(df):
    buy_signal = (df['rsi'] < 30) & (df['rsi'].shift(1) >= 30)
    sell_signal = (df['rsi'] > 70) & (df['rsi'].shift(1) <= 70)
    return buy_signal, sell_signal

def generate_signals_stochrsi(df):
    overbought = 80
    oversold = 20

    # Create boolean masks for overbought and oversold levels
    is_overbought = df['stochrsi'] > overbought
    is_oversold = df['stochrsi'] < oversold
    return is_overbought, is_oversold
#
#
#

# EMA
def _ema_n(df, n):
    close_price = df['close']
    ema_n = calculate_ema(df, n)
    ema_n = ema_n.round(3)
    df['ema_{}'.format(n)] = ema_n
    return df

# VWAP
def _vwap(df, label='vwap', window=3, fillna=True):
        vwap_hcl3 = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df["close"], volume=df['volume'], window=window, fillna=fillna).volume_weighted_average_price()
        df[label] = vwap_hcl3
        buy_signal, sell_signal = generate_signals_vwap(df)

        # Add signals to the DataFrame
        df['vwap_buy_signal'] = buy_signal.astype(int)
        df['vwap_sell_signal'] = sell_signal.astype(int)

        return df

# RSI 
def _rsi(df):
    rsi = ta.momentum.rsi(df['close'], window=14) # to add length add , length=6 default 14
    df['rsi'] = rsi
    buy_signal, sell_signal = generate_signals_rsi(df)

    # Add signals to the DataFrame
    df['rsi_buy_signal'] = buy_signal.astype(int)
    df['rsi_sell_signal'] = sell_signal.astype(int)
    return df

# stochastic RSI 
def _stochrsi(df):
    stochrsi = ta.stochrsi(df['close'])
    df['stochrsi'] = stochrsi
    is_overbought, is_oversold = generate_signals_stochrsi(df)

    # Add overbought and oversold signals to the DataFrame
    df['stochrsi_sell_signal'] = is_overbought.astype(int)
    df['stochrsi_buy_signal'] = is_oversold.astype(int)
    return df

# MACD 
def _macd(df):
    macd = ta.macd(df['close'])

    # Create a column for MACD histogram
    macd_histogram = macd['MACDh']

    # Identify buy and sell signals
    buy_signal = macd['MACD'] > macd['SIGNAL']
    sell_signal = macd['MACD'] < macd['SIGNAL']

    # Add buy and sell signals to the DataFrame
    df['macd_buy_signal'] = buy_signal.astype(int)
    df['macd_sell_signal'] = sell_signal.astype(int)

    return df
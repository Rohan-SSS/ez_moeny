# Imports
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta.volume import VolumeWeightedAveragePrice

# Price change with %-------------------------------
def price_change(df):
    df['price_change'] = df['close'] - df['close'].shift(1)
    df['price_pct_change'] = df['price_change'] / df['close'].shift(1) * 100

    df['open_change'] = df['open'] - df['open'].shift(1)
    df['open_pct_change'] = df['open_change'] / df['open'].shift(1) * 100

    df['high_change'] = df['high'] - df['high'].shift(1)
    df['high_pct_change'] = df['high_change'] / df['high'].shift(1) * 100

    df['low_change'] = df['low'] - df['low'].shift(1)
    df['low_pct_change'] = df['low_change'] / df['low'].shift(1) * 100

    df['close_change'] = df['close'] - df['close'].shift(1)
    df['close_pct_change'] = df['close_change'] / df['close'].shift(1) * 100

    df['volume_change'] = df['volume'] - df['volume'].shift(1)
    df['volume_pct_change'] = df['volume_change'] / df['volume'].shift(1) * 100

    return df



# EMA--------------------------------------------

def calculate_ema(data, n):
    ema = data.close.ewm(span=n, adjust=False).mean()
    return ema

def ema_n(df, n):
    close_price = df['close']
    ema_n = calculate_ema(df, n)
    ema_n = ema_n.round(6)
    df['ema_{}'.format(n)] = ema_n
    return df

def ema_signal(df):
    diff100 = (df['close'] - df['ema_100'])/df['ema_100']
    diff200 = (df['close'] - df['ema_200'])/df['ema_200']
    # Create the signal column
    signal = pd.Series(0, index=df.index)
    signal[(diff100 > 0.0025) & (diff200 > 0.002)] = 1
    signal[(diff100 < -0.0025) & (diff200 < -0.002)] = -1

    df['ema_signal'] = signal
    
    return df


# VWAP-----------------------------------------------

def generate_signal_vwap(df):
    signal = pd.Series(data=np.zeros(len(df)), index=df.index)
    signal[df['close'] > (df['vwap'] + (0.0005 * df['close']))] = 1
    signal[df['close'] < (df['vwap'] - (0.0005 * df['close']))] = -1
    return signal.astype(int)

def vwap(df, label='vwap', window=3, fillna=True):
    vwap_hcl3 = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=window, fillna=fillna).volume_weighted_average_price()
    df[label] = vwap_hcl3
    signal = generate_signal_vwap(df)
    df['vwap_signal'] = signal
    return df


# Stochastic RSI--------------------------------------

def stochrsi(df, overbought=80, oversold=20):
    # Calculate Stochastic RSI
    stochrsi = df.ta.stoch(high='high', low='low', close='close', k=14, d=3, append=True)

    # Create boolean masks for overbought and oversold levels
    is_overbought = (stochrsi['STOCHk_14_3_3'] > overbought) & (stochrsi['STOCHd_14_3_3'] > overbought) & (stochrsi['STOCHk_14_3_3'] < stochrsi['STOCHd_14_3_3'])
    is_oversold = (stochrsi['STOCHk_14_3_3'] < oversold) & (stochrsi['STOCHd_14_3_3'] < oversold) & (stochrsi['STOCHk_14_3_3'] > stochrsi['STOCHd_14_3_3'])

    # Reindex the boolean masks to align them
    is_overbought = is_overbought.reindex(df.index, fill_value=False)
    is_oversold = is_oversold.reindex(df.index, fill_value=False)

    # Create the signal column
    signal = pd.Series(np.zeros(len(df)), index=df.index)
    signal[is_overbought] = -1
    signal[is_oversold] = 1

    # Add the signal column to the DataFrame
    df['stochrsi_signal'] = signal.astype(int)
    return df

# MACD -------------------------------------------------

def macd(df):
    macd = ta.macd(df['close'])
    df['MACD_12_26_9'] = macd['MACD_12_26_9']
    df['MACDs_12_26_9'] = macd['MACDs_12_26_9']
    df['MACDh_12_26_9'] = macd['MACDh_12_26_9']
    # Create a signal column based on buy and sell signals
    signal = np.zeros(len(df))
    signal[macd['MACD_12_26_9'] > macd['MACDs_12_26_9']] = 1
    signal[macd['MACD_12_26_9'] < macd['MACDs_12_26_9']] = -1

    # Add signal column to the DataFrame
    df['macd_signal'] = signal
    df['macd_signal'] = df['macd_signal'].astype(int)
    return df

# Trend -------------------------------------------------
def get_trend(df):
    # Calculate the percentage change in price for the current candlestick and the next 7 candlesticks
    pct_change = df['close'].pct_change(periods=7)
    
    # Initialize the trend column with 0 (neutral)
    df['trend'] = 0
    
    # Set the trend to 1 (up) if the price is up by 0.2% or more in any of the next 7 candlesticks
    df.loc[pct_change >= 0.002, 'trend'] = 1
    
    # Set the trend to -1 (down) if the price is down by 0.2% or more in any of the next 7 candlesticks
    df.loc[pct_change <= -0.002, 'trend'] = -1
    
    return df
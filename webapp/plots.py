import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

import streamlit as st

plt.style.use("dark_background")

def plot_chart(df):
    width = 0.6   # width of real body
    width2 = 0.05  # width of shadow
    offset = 0.2  # offset between adjacent bars

    fig, ax = plt.subplots(figsize=(24, 12))

    # find the rows that are bullish
    dfup = df[df.close >= df.open]
    # find the rows that are bearish
    dfdown = df[df.close < df.open]

    # plot the bullish candle stick with an offset
    ax.bar(dfup.index - offset/2, dfup.close - dfup.open, width,
        bottom=dfup.open, edgecolor='w', color='green')
    ax.bar(dfup.index - offset/2, dfup.high - dfup.close, width2,
        bottom=dfup.close, edgecolor='w', color='green')
    ax.bar(dfup.index - offset/2, dfup.low - dfup.open, width2,
        bottom=dfup.open, edgecolor='w', color='green')

    # plot the bearish candle stick with an offset
    ax.bar(dfdown.index + offset/2, dfdown.close - dfdown.open, width,
        bottom=dfdown.open, edgecolor='w', color='red')
    ax.bar(dfdown.index + offset/2, dfdown.high - dfdown.open, width2,
        bottom=dfdown.open, edgecolor='w', color='red')
    ax.bar(dfdown.index + offset/2, dfdown.low - dfdown.close, width2,
        bottom=dfdown.close, edgecolor='w', color='red')
    ax.grid(color='gray')

    plt.plot(df.EMA_100, 'white')
    plt.plot(df.EMA_200, 'grey')
    plt.plot(df.VWAP, 'blue')


def plot_res(predictions, y):
    plt.figure(figsize=(30,4))
    plt.plot(predictions[:100], 'g')
    plt.plot((y[:100]),  'r')
    plt.axhline(y=0, color='black', linestyle='--')
    plt.show

def interactive_chart(df):
    df.columns = [x.lower() for x in df.columns]

    # Create our primary chart
    # the rows/cols arguments tell plotly we want two figures
    fig = make_subplots(rows=1, cols=1)  

    # Create our Candlestick chart with an overlaid price line
    fig.append_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
           

        ), row=1, col=1  # <------------ upper chart
    )

    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )
    fig.update_layout(layout)

    # View our chart in the Streamlit app
    st.plotly_chart(fig)


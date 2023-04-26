import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.renderers.default='browser'

def get_candlestick_plot(
        df: pd.DataFrame,
        ticker: str
):
    '''
    Create the candlestick chart with two moving avgs + a plot of the volume
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    ma1 : int
        The length of the first moving average (days)
    ma2 : int
        The length of the second moving average (days)
    ticker : str
        The ticker we are plotting (for the title).
    '''
    
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.1,
        subplot_titles = (f'{ticker} Stock Price', 'Volume Chart'),
        row_width = [0.3, 0.7]
    )

    fig.add_trace(
        go.Candlestick(
            x = df['time'],
            open = df['open'], 
            high = df['high'],
            low = df['low'],
            close = df['close']
        ),
        row = 1,
        col = 1,
    )
    fig.add_trace(
        go.Bar(x = df['time'], y = df['volume'], name = 'volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['xaxis2']['title'] = 'time'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    
    fig.update_xaxes(
        rangebreaks = [dict(bounds=["sat", "mon"]),  
                        dict(bounds=[16, 9.5], pattern="hour")],
        rangeslider_visible = False,
    )

    fig.update_layout(width=1200, height=600)
    
    return fig

def get_candlestick_chart(ticker, df: pd.DataFrame):
        fig = get_candlestick_plot(df[-120:], f'{ticker}')
        return fig


def get_pred_chart(real, cmp):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(cmp[-120:]))), y=cmp[-120:], mode='lines', name='Real'))
    fig.add_trace(go.Scatter(x=list(range(len(real[-120:]))), y=real[-120:], mode='lines', name='Predicted', line=dict(color='red', dash='dash')))
    fig.update_layout(width=1200, height=400)
    return fig
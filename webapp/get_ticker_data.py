import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def get_ticker_data(ticker):
    """
    This fucntion uses Meta Trader 5 application to fetch the real time data needed to make predictions
    """
    mt5.initialize()
    # Compute now date
    from_date = datetime.now()

    # Extract n Ticks before now
    rates = mt5.copy_rates_from(f"{ticker}", mt5.TIMEFRAME_M30, from_date, 1000)

    # Transform Tuple into a DataFrame
    df_rates = pd.DataFrame(rates)

    # Convert number format of the date into date format
    df_rates["time"] = pd.to_datetime(df_rates["time"], unit="s")
    df_rates = df_rates.drop(['spread', 'real_volume'], axis=1)
    df_rates.rename(columns={"tick_volume":"volume"}, inplace=True)
    return df_rates


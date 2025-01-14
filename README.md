# EZ Money
> Predicts the possible trend of an asset

## Project Description
This project aimes to predict the possible trend of an asset, the defination of trend being that the asset moves up or down by 0.25% in the next 7 candles of 30 minutes and the prediction is a binary outcome scaled to up, down  or neutral.
The LSTM model is used with a set of features which includes a bunch of indicators mainly used for day trading like EMAs, MACD, Stochastic RSI, VWAP etc., The data used for training and testing was of EURUSD currency pair which had 100,000 rows of OHLC data with volume.

## Installation

Clone the project
```bash
git clone https://github.com/Rohan-SSS/ez_money
cd ez_money
```

Create virtual environment and install dependencies
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Note: You also need to install Meta Trader 5 application on windows or Use third party APIs like alphavantage to fetch the data needed at time of prediction, there is already a file for this, just set your api key in it.

## Usage

Run the streamlit app to see the predictions
```bash
cd webapp
streamlit run webapp.py
```


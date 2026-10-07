# Import modules
import yfinance as yf
import pandas as pd
import requests
import csv
import zipfile
from io import BytesIO, StringIO
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from util.constants import *


# get ticker object
def get_yfinance_ticker_obj(ticker_symbol):
    # ticker_symbol = "IDFCFIRSTB.NS"  # AAPL'  # Example: Apple Inc. (AAPL)
    try:
        ticker_obj = yf.Ticker(ticker_symbol)
    except Exception as e:
        print(f"Failed to get ticker object {e}")
    return ticker_obj


# get ticker object history
def get_yfinance_ticker_history(ticker_symbol, ticker_period):
    try:
        ticker_history = ticker_symbol.history(period=ticker_period)

    except Exception as e:
        print(f"Failed to get ticker history {e}")
    return ticker_history


# get ticker object history period
def get_yfinance_ticker_history_period(
    ticker_symbol, ticker_period_start, ticker_period_end
):
    try:
        ticker_history = ticker_symbol.history(
            start=ticker_period_start, end=ticker_period_end
        )
    except Exception as e:
        print(f"Failed to get ticker history {e}")
    return ticker_history


# get ticker object history period
# intervals = ['1d', '1wk', '1mo', '3mo']
# periods   = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd']#, 'max']
def get_yfinance_ticker_history_period_interval(ticker_symbol, inter_val, period_val):
    try:
        ticker_history = ticker_symbol.history(interval=inter_val, period=period_val)
    except Exception as e:
        print(f"Failed to get ticker history {e}")
    return ticker_history


def get_yfinance_ticker_info(ticker_symbol):
    ticker_info_df = pd.DataFrame()
    try:
        ticker_info = ticker_symbol.info
        ticker_info_df = pd.DataFrame([ticker_info])
        ticker_info_df["date_created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticker_info_df["symbol_name"] = ticker_symbol  # main_symbol
        ticker_info_df["date_id"] = datetime.now().strftime("%Y%m%d")

    except Exception as e:
        print(f"Failed to get ticker information {e}")
    return ticker_info_df


def get_yfinance_ticker_financials(ticker_symbol):
    try:
        ticker_fin = ticker_symbol.financials
    except Exception as e:
        print(f"Failed to get ticker financials {e}")
    return ticker_fin


def get_yfinance_ticker_action(ticker_symbol):
    try:
        ticker_actions = ticker_symbol.actions
    except Exception as e:
        print(f"Failed to get ticker financials {e}")
    return ticker_actions


def get_yfinance_ticker_news(ticker_symbol):
    try:
        ticker_news = ticker_symbol.news
    except Exception as e:
        print(f"Failed to get ticker News {e}")
    return ticker_news


def get_yfinance_ticker_cashflow(ticker_symbol):
    try:
        ticker_cashflow = ticker_symbol.cashflow
    except Exception as e:
        print(f"Failed to get ticker cashflow {e}")
    return ticker_cashflow


def get_yfinance_tickers(ticker_list):
    try:
        data = yf.download(tickers=ticker_list, threads=True, group_by="ticker")
        data = data.T
    except Exception as e:
        print(f"Failed to get ticker financials {e}")
    return data

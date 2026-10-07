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


# get list of all equity available to trade in NSE, return pd data frame
def get_nse_equity_list():
    try:
        data_df = pd.read_csv(
            "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        )

    except Exception as e:
        raise FileNotFoundError(f" Equity List not found :: NSE error : {e}")
    data_df = data_df[
        [
            "SYMBOL",
            "NAME OF COMPANY",
            " SERIES",
            " DATE OF LISTING",
            " PAID UP VALUE",
            " MARKET LOT",
            " ISIN NUMBER",
            " FACE VALUE",
        ]
    ]
    return data_df


def get_urlfetch(url):
    r_session = requests.session()
    nse_live = r_session.get("http://nseindia.com", headers=header)
    return r_session.get(url, headers=header)


def get_url_content(url_link):
    var_dataframe = ""
    url = url_link

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()  # Ensure we notice bad responses
        dfa = pd.read_html(response.text)[0]
    except Exception as e:
        print(f"URL request is failed  {e}")
    return dfa


def get_nse_stock_bhav_copy_equities_legancy(trade_date: str):
    trade_date = trade_date.strftime("%d-%b-%Y")
    print(trade_date)
    url = (
        f"https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22CM-UDiFF%20Common%20Bhavcopy%20Final%20(zip)%22%2C%22type%22%3A%22daily-reports%22%2C%22category%22%3A%22capital-market%22%2C%22section%22%3A%22equities%22%7D%5D&type=equities&mode=single&date="
        + trade_date
    )
    ## print(url)

    request_bhav = get_urlfetch(url)
    df = pd.DataFrame()
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), "r")
        for file_name in zip_bhav.filelist:
            if file_name:
                df = pd.read_csv(zip_bhav.open(file_name))
                for col in df.columns:
                    if col in bhav_copy_Column_list:
                        bhav_df[col] = df[col]
                    elif col == "Rsvd01":
                        bhav_df["Rsvd1"] = df[col]
                    elif col == "Rsvd02":
                        bhav_df["Rsvd2"] = df[col]
                    elif col == "Rsvd03":
                        bhav_df["Rsvd3"] = df[col]
                    elif col == "Rsvd04":
                        bhav_df["Rsvd4"] = df[col]
                    else:
                        print(
                            f"This column data is not inserting to db {col}: {df[col]}"
                        )
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f" Data not found, change the date...")
    return bhav_df


def get_nse_stock_bhav_copy_equities(trade_date: str):
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = "https://archives.nseindia.com/content/historical/EQUITIES/"
    payload = (
        f"{str(trade_date.strftime('%Y'))}/{str(trade_date.strftime('%b').upper())}/"
        f"cm{str(trade_date.strftime('%d%b%Y').upper())}bhav.csv.zip"
    )
    request_bhav = get_urlfetch(url + payload)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), "r")
        for file_name in zip_bhav.filelist:
            if file_name:
                bhav_df = pd.read_csv(zip_bhav.open(file_name))
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f" Data not found, change the date...")
    bhav_df = bhav_df[
        [
            "SYMBOL",
            "SERIES",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "LAST",
            "PREVCLOSE",
            "TOTTRDQTY",
            "TOTTRDVAL",
            "TIMESTAMP",
            "TOTALTRADES",
        ]
    ]
    return bhav_df

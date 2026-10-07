# Import modules
import yfinance as yf
import pandas as pd
import requests
import csv
import zipfile
import math
import numpy as np
from io import BytesIO, StringIO
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from util.constants import *
from mftool import Mftool
from io import StringIO
import openpyxl


def get_all_mutalfund_details():
    url = "https://portal.amfiindia.com/DownloadSchemeData_Po.aspx?mf=0"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        df = pd.read_csv(StringIO(data), sep=",", engine="python")

        # Print the first few rows
        # print(df.head())

        df_temp = df.rename(
            columns={
                "AMC": "amc",
                "Code": "scheme_code",
                "Scheme Name": "scheme_name",
                "Scheme Type": "scheme_type",
                "Scheme Category": "scheme_category",
                "Scheme NAV Name": "scheme_nav_name",
                "Scheme Minimum Amount": "scheme_minimum_amount",
                "Launch Date": "launch_date",
                " Closure Date": "closure_date",
                "ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment": "isin_div_payout_isin_growth_isin_div_reinvestment",
            },
            inplace=False,
        )

        return df_temp
    else:
        print(f"Error fetching data. Status code: {response.status_code}")


def get_mutalfund_present_nav_all():
    url = "https://www.amfiindia.com/spages/NAVAll.txt"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        df = pd.read_csv(StringIO(data), sep=";", engine="python")
        df_tmp = df.rename(
            columns={
                "Scheme Code": "scheme_code",
                "ISIN Div Payout/ ISIN Growth": "isin_div_payout_isin_growth",
                "ISIN Div Reinvestment": "isin_div_reinvestment",
                "Scheme Name": "scheme_name",
                "Net Asset Value": "net_asset_value",
                "Date": "date_nav",
            },
            inplace=False,
        )

        df_tmp["date_nav"] = pd.to_datetime(df_tmp["date_nav"]).dt.date
        df_tmp["date_nav_id"] = pd.to_datetime(df_tmp["date_nav"]).dt.strftime("%Y%m%d")

        return df_tmp[df_tmp["date_nav"].notna()]
    else:
        print(f"Error fetching data. Status code: {response.status_code}")


def get_mutal_fund_nav_history(scheme_code):
    # Step 1: Fetch the JSON data from the API
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(url)
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Step 2: Convert the JSON data into a Python dictionary
        json_data = response.json()

        if json_data["meta"] == {}:
            return pd.DataFrame()

        fund_info = json_data["meta"]
        fund_nav_hisotry = json_data["data"]
        data_df = pd.DataFrame(fund_nav_hisotry)

        tmp_val = fund_info["fund_house"]
        data_df["fund_house"] = tmp_val

        tmp_val = fund_info["scheme_type"]
        data_df["scheme_type"] = tmp_val

        tmp_val = fund_info["scheme_category"]
        data_df["scheme_category"] = tmp_val

        tmp_val = fund_info["scheme_code"]
        data_df["scheme_code"] = tmp_val

        tmp_val = fund_info["scheme_name"]
        data_df["scheme_name"] = tmp_val

        tmp_val = fund_info["isin_growth"]
        data_df["isin_growth"] = tmp_val

        tmp_val = fund_info["isin_div_reinvestment"]
        data_df["isin_div_reinvestment"] = tmp_val

        data_df["date_nav_id"] = pd.to_datetime(
            data_df["date"], format="%d-%m-%Y"
        ).dt.strftime("%Y%m%d")

        # data_df = data_df.merge(meta_df, on="scheme_code", how="left")
        # data_df["min_nav"] = data_df["nav"].min()
        # data_df["max_nav"] = data_df["nav"].max()
        # Calculate cumulative returns
        # df['daily_returns'] = df['nav'].pct_change()
        # df['cumulative_returns'] = (df['daily_returns']+1).cumprod()
        # Method 1
        # (df['cumulative_returns'].iloc[-1] - 1)*100

        # Method 2
        # ((df['nav'].iloc[-1]/df['nav'].iloc[0]) - 1)*100

        # n_years = 3
        # ((df['nav'].iloc[-1]/df['nav'].iloc[0]) ** (1/n_years) - 1) * 100

        # CAGR
        # df = (df.sort_values(date_col).query(f"{date_col} >= @start_date and {date_col} <=@end_date").assign(daily_returns=lambda x: x[nav_col].pct_change(),cumulative_daily_returns=lambda x: (x['daily_returns'] + 1).cumprod()).reset_index(drop=True))

        # absolute_returns_prcnt = (mf_with_cumulative['cumulative_daily_returns'].values[-1] - 1) * 100
        # cagr = ((mf_with_cumulative['nav'].iloc[-1]/mf_with_cumulative['nav'].iloc[0]) ** (1/n_years) - 1) * 100

        #  df['dayChange'] = df['nav'].astype(float).diff(periods=-1)

        # data_df["mean"] = data_df["nav"].mean() this not working becasue of string later need calculate
        # data_df["Start_date"] = data_df["date"].min()
        # data_df["last_date"] = data_df["date"].max()

        return data_df
    else:
        print("Failed to fetch data:", response.status_code)


def get_mutal_fund_nav_history_from_dt(scheme_code, frm_date):
    # Step 1: Fetch the JSON data from the API
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(url)
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Step 2: Convert the JSON data into a Python dictionary
        json_data = response.json()

        if json_data["meta"] == {}:
            return pd.DataFrame()

        fund_info = json_data["meta"]
        fund_nav_hisotry = json_data["data"]
        data_df = pd.DataFrame(fund_nav_hisotry)

        tmp_val = fund_info["fund_house"]
        data_df["fund_house"] = tmp_val

        tmp_val = fund_info["scheme_type"]
        data_df["scheme_type"] = tmp_val

        tmp_val = fund_info["scheme_category"]
        data_df["scheme_category"] = tmp_val

        tmp_val = fund_info["scheme_code"]
        data_df["scheme_code"] = tmp_val

        tmp_val = fund_info["scheme_name"]
        data_df["scheme_name"] = tmp_val

        tmp_val = fund_info["isin_growth"]
        data_df["isin_growth"] = tmp_val

        tmp_val = fund_info["isin_div_reinvestment"]
        data_df["isin_div_reinvestment"] = tmp_val

        data_df["date_nav_id"] = pd.to_datetime(
            data_df["date"], format="%d-%m-%Y"
        ).dt.strftime("%Y%m%d")

        data_df = data_df[data_df["date_nav_id"] > frm_date].sort_values(
            by="date_nav_id", ascending=True
        )

        return data_df
    else:
        print("Failed to fetch data:", response.status_code)


def get_all_mutalfund_aum():
    url = "https://www.valueresearchonline.com/amfi/fund-performance-data/?end-type=3&primary-category=SDT&category=SDT_SD&amc=ALL&nav-date=03-Jan-2025"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text

        # Print the first few rows
        print(data)

        return "kk"
    else:
        print(f"Error fetching data. Status code: {response.status_code}")


# https://www.amfiindia.com/research-information/aum-data/average-aum
# https://www.amfiindia.com/Themes/Theme1/downloads/AverageMarketCapitalizationoflistedcompaniesduringthesixmonthsended31Dec2024.xlsx


def get_mutalfund_all_nav_history_tp1():
    url = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=01-Dec-2007&todt=30-Dec-2024"
    response_1 = requests.get(url)

    if response_1.status_code == 200:
        data = response_1.text
        df = pd.read_csv(StringIO(data), sep=";", engine="python")

        # Print the first few rows
        print(df.head())

        return df
    else:
        print(f"Error fetching data. Status code: {response_1.status_code}")


def get_mutalfund_all_nav_history_tp2():

    url = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=2&frmdt=01-Dec-2007&todt=30-Dec-2024"
    response_2 = requests.get(url)

    if response_2.status_code == 200:
        data = response_2.text
        df = pd.read_csv(StringIO(data), sep=";", engine="python")
        return df
    else:
        print(f"Error fetching data. Status code: {response_2.status_code}")


def get_mutalfund_all_nav_history_tp3():
    url = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=3&frmdt=01-Dec-2007&todt=30-Dec-2024"
    response_3 = requests.get(url)

    if response_3.status_code == 200:

        data = response_3.text
        df = pd.read_csv(StringIO(data), sep=";", engine="python")

        # Print the first few rows
        print(df.head())

        return df
    else:
        print(f"Error fetching data. Status code: {response_3.status_code}")


def get_all_mutal_fund_list():
    mf = Mftool()
    result = mf.get_available_schemes("")
    df = pd.DataFrame(list(result.items()), columns=["Key", "Value"])
    # Key : Schema_code,  Value:Schema_Name
    df.drop(0)
    df1 = df.sort_values(by="Key", ascending=True)
    return df1
    ## .to_string(header=False, index=False)


def get_all_mutal_fund_search(mf, mutual_fund_pattern):
    # mf = Mftool()
    result = mf.get_available_schemes(mutual_fund_pattern)
    df = pd.DataFrame(list(result.items()), columns=["Key", "Value"])
    return df.to_string(header=False, index=False)


def get_mutual_fund_details(mf, mutual_fund_code):
    mf_d = Mftool()
    result = mf_d.get_scheme_details(mutual_fund_code)
    # Flatten the dictionary
    flattened_result = {
        "fund_house": result["fund_house"],
        "scheme_type": result["scheme_type"],
        "scheme_category": result["scheme_category"],
        "scheme_code": result["scheme_code"],
        "scheme_name": result["scheme_name"],
        "scheme_start_date": result["scheme_start_date"]["date"],
        "scheme_listed_nav": result["scheme_start_date"]["nav"],
    }
    df = pd.DataFrame([flattened_result])

    return df


def get_mutual_fund_Nav_updated_on(mf, mutual_fund_code):
    # mf = Mftool()
    result = mf.get_scheme_quote(mutual_fund_code)
    df = pd.DataFrame([result])
    return df


def get_mutual_fund_Nav_history(mf, mutual_fund_code):
    # mf = Mftool()
    df = (
        mf.get_scheme_historical_nav(mutual_fund_code, as_Dataframe=True)
        .reset_index()
        .assign(
            nav=lambda x: x["nav"].astype(float),
            date=lambda x: pd.to_datetime(x["date"], format="%d-%m-%Y"),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )
    df["scheme_code"] = mutual_fund_code
    # Calculate cumulative returns
    df["daily_returns"] = df["nav"].pct_change()
    df["cumulative_returns"] = (df["daily_returns"] + 1).cumprod()
    df["sma5"] = df["nav"].rolling(window=5).mean()
    df["sma9"] = df["nav"].rolling(window=9).mean()
    df["sma15"] = df["nav"].rolling(window=15).mean()
    df["sma30"] = df["nav"].rolling(window=30).mean()

    return df


def get_mutual_fund_Nav_history_for_period(mf, mutual_fund_code, start_date, end_date):
    # mf = Mftool()
    # start_date = pd.to_datetime("1-1-2021", format="%d-%m-%Y")
    # end_date = pd.to_datetime("31-12-2023", format="%d-%m-%Y")

    df = (
        mf.get_scheme_historical_nav(mutual_fund_code, as_Dataframe=True)
        .reset_index()
        .assign(
            nav=lambda x: x["nav"].astype(float),
            date=lambda x: pd.to_datetime(x["date"], format="%d-%m-%Y"),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )
    df = df.query("date >= @start_date and date <=@end_date").reset_index(drop=True)
    df["scheme_code"] = mutual_fund_code
    # Calculate cumulative returns
    df["daily_returns"] = df["nav"].pct_change()
    df["cumulative_returns"] = (df["daily_returns"] + 1).cumprod()

    return df

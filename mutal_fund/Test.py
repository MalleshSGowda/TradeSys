from mftool import Mftool
import math
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

n_years = 3  # Parameter for historical years

# Get from and to dates
from_date = datetime.datetime.strptime("1-1-2021", "%d-%m-%Y").date()
to_date = datetime.datetime.strptime("31-1-2023", "%d-%m-%Y").date()
print(from_date, to_date)


def convert_to_date(date_str):
    date_obj = datetime.datetime.strptime(date_str, "%d %b %Y")
    return date_obj


def fetch_mutual_fund_data(mutual_fund_code):
    mf = Mftool()
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

    return df


def get_cumulative_returns(
    df,
    nav_col="CLOSE",
    date_col="date",
    starting_date="1-1-2019",
    ending_date="20-1-2023",
):
    start_date = pd.to_datetime(starting_date, format="%d-%m-%Y")
    end_date = pd.to_datetime(ending_date, format="%d-%m-%Y")

    df = (
        df.sort_values(date_col)
        .query(f"{date_col} >= @start_date and {date_col} <=@end_date")
        .assign(
            daily_returns=lambda x: x[nav_col].pct_change(),
            cumulative_daily_returns=lambda x: (x["daily_returns"] + 1).cumprod(),
        )
        .reset_index(drop=True)
    )

    return df


def SMA(mf_data_dict):
    days = 30
    mf_data_dict["nav"] = mf_data_dict["nav"].astype(float)
    print("==========")
    print(mf_data_dict["nav"])
    print("==========")
    pred = []
    for i in range(days):
        value = mf_data_dict["nav"][i : len(mf_data_dict)].sum() + sum(pred)
        pred.append(round(value / len(mf_data_dict), 5))
        print("===", mf_data_dict["nav"][i : len(mf_data_dict)].sum(), sum(pred))
    print("SMA 30", pred)
    return pred


def SMA30(mf_data_dict):
    days = len(mf_data_dict)
    mf_data_dict["nav"] = mf_data_dict["nav"].astype(float)

    pred = []
    for i in range(0, len(mf_data_dict) - 5, 1):
        value = mf_data_dict["nav"][i : i + 5].sum().astype(float)
        print("SMA 30", mf_data_dict["nav"][i], " -- ", value, ":", value / 5)
    return mf_data_dict


def SMA_days(mf_data_dict, days):
    day = days
    smadays = "SMA" + str(days)
    mf_data_dict["nav"] = mf_data_dict["nav"].astype(float)

    pred = []
    for i in range(0, len(mf_data_dict) - day, 1):
        value = mf_data_dict["nav"][i : i + day].sum()
        print("SMA 30", mf_data_dict["nav"][i], " -- ", value, ":", value / day)
        mf_data_dict[smadays] = value / day
    return mf_data_dict


mutual_funds = {
    "125307": "PGIM India Midcap Opportunities Fund - Direct Plan - Growth Option",
}

mf_data_dict = dict()
for mutual_fund_code, mutual_fund_desc in mutual_funds.items():
    print(mutual_fund_desc)

    df = fetch_mutual_fund_data(mutual_fund_code)

    df.sort_values(by='date')

    df["sma5"] = df["nav"].rolling(window=5).mean()

    print(df)

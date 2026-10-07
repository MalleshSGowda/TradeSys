import yfinance as yf
import pandas as pd
from datetime import datetime
from util.util import *

var_engine = get_engine("localhost", "src_db", "root", "root")

table_name = "yfinance_company_financial"

truncate_table(table_name, var_engine)

query = """SELECT distinct ticker FROM trading.stock order by ticker asc;"""

# Create a connection and execute the query
with var_engine.connect() as conn:
    result = conn.execute(text(query))

# Iterate over the results and print each SYMBOL
for row in result:
    print(f"SYMBOL: {row[0]}")
    # Define the symbol of the company for which you want to fetch data
    main_symbol = (
        row[0] + ".NS"
    )  # IDFC First Bank IDFCFIRSTB  ITALIANE 3IINFOTECH AGRITECH 5PAISA

    Column_list = [
        "52WeekChange",
        "averageDailyVolume10Day",
        "averageVolume",
        "averageVolume10days",
        "beta",
        "bookValue",
        "city",
        "companyOfficers",
        "country",
        "currency",
        "currentPrice",
        "currentRatio",
        "date_created",
        "dayHigh",
        "dayLow",
        "debtToEquity",
        "ebitda",
        "enterpriseToEbitda",
        "enterpriseToRevenue",
        "enterpriseValue",
        "exchange",
        "exDividendDate",
        "fax",
        "fiftyDayAverage",
        "fiftyTwoWeekHigh",
        "fiftyTwoWeekLow",
        "financialCurrency",
        "firstTradeDateEpochUtc",
        "floatShares",
        "freeCashflow",
        "gmtOffSetMilliseconds",
        "grossMargins",
        "heldPercentInsiders",
        "impliedSharesOutstanding",
        "industry",
        "industryDisp",
        "industryKey",
        "lastDividendDate",
        "lastDividendValue",
        "lastFiscalYearEnd",
        "longBusinessSummary",
        "longName",
        "marketCap",
        "maxAge",
        "messageBoardId",
        "mostRecentQuarter",
        "netIncomeToCommon",
        "nextFiscalYearEnd",
        "open",
        "operatingCashflow",
        "operatingMargins",
        "phone",
        "previousClose",
        "priceHint",
        "priceToBook",
        "priceToSalesTrailing12Months",
        "profitMargins",
        "quickRatio",
        "quoteType",
        "recommendationKey",
        "regularMarketDayHigh",
        "regularMarketDayLow",
        "regularMarketOpen",
        "regularMarketPreviousClose",
        "regularMarketVolume",
        "returnOnAssets",
        "returnOnEquity",
        "revenueGrowth",
        "revenuePerShare",
        "SandP52WeekChange",
        "sector",
        "sectorDisp",
        "sectorKey",
        "sharesOutstanding",
        "shortName",
        "symbol",
        "symbol_name",
        "timeZoneFullName",
        "timeZoneShortName",
        "totalCash",
        "totalCashPerShare",
        "totalDebt",
        "totalRevenue",
        "trailingEps",
        "trailingPE",
        "trailingPegRatio",
        "twoHundredDayAverage",
        "underlyingSymbol",
        "uuid",
        "volume",
        "website",
        "zip",
    ]

    # Fetch the main company data  object

    yf_tkr_obj = get_yfinance_ticker_obj(main_symbol)

    # Get the company's info
    info = yf_tkr_obj.info

    # Convert the info dictionary to a DataFrame
    df = pd.DataFrame([info])
    dfa = pd.DataFrame()

    # Convert any complex types (like dictionaries) to strings
    for col in df.columns:
        if col in Column_list:
            if isinstance(df[col].iloc[0], (dict, list)):
                df[col] = df[col].apply(lambda x: str(x))
                dfa[col] = df[col].apply(lambda x: str(x))
            else:
                # print(f" ** {col} : {df[col].values}")
                dfa[col] = df[col]

    # Add a custom attribute or additional columns if needed

    dfa["date_created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dfa["symbol_name"] = row[0]  # main_symbol
    dfa["date_id"] = datetime.now().strftime("%Y%m%d")

    # Write the DataFrame to the database
    try:
        # df.to_sql(name=table_name1, con=engine, if_exists="append", index=False)
        # print(dfa)
        dfa.to_sql(name=table_name, con=var_engine, if_exists="append", index=False)
        print("Data successfully written to MySQL.")

    except Exception as e:
        print(f"Error writing data to MySQL: {e}")

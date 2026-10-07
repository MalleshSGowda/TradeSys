import os

dd_mm_yyyy = '%d-%m-%Y'
dd_mmm_yyyy = '%d-%b-%Y'
ddmmyyyy = '%d%m%Y'
mmm_yy = '%b-%y'

equity_periods = ['1D', '1W', '1M', '3M', '6M', '1Y']
indices_list = ['NIFTY','FINNIFTY','BANKNIFTY']


# ---------- column lists-----------------

price_volume_and_deliverable_position_data_columns = \
    ['Symbol', 'Series', 'Date', 'PrevClose', 'OpenPrice', 'HighPrice',
     'LowPrice', 'LastPrice', 'ClosePrice', 'AveragePrice', 'TotalTradedQuantity',
     'TurnoverInRs', 'No.ofTrades', 'DeliverableQty', '%DlyQttoTradedQty']

price_volume_data_columns = ['Symbol', 'Series', 'Date', 'PrevClose', 'OpenPrice', 'HighPrice',
                             'LowPrice', 'LastPrice', 'ClosePrice', 'AveragePrice',
                             'TotalTradedQuantity', 'Turnover', 'No.ofTrades']

deliverable_data_columns = ['Symbol', 'Series', 'Date', 'TradedQty', 'DeliverableQty', '%DlyQttoTradedQty']

bulk_deal_data_columns = ['Date', 'Symbol', 'SecurityName', 'ClientName', 'Buy/Sell', 'QuantityTraded',
                          'TradePrice/Wght.Avg.Price', 'Remarks']

block_deals_data_columns = ['Date', 'Symbol', 'SecurityName', 'ClientName', 'Buy/Sell', 'QuantityTraded',
                            'TradePrice/Wght.Avg.Price', 'Remarks']

short_selling_data_columns = ['Date', 'Symbol', 'SecurityName', 'Quantity']

bhavcopy_old = ['TradDt', 'ISIN', 'TckrSymb', 'SctySrs', 'OpnPric', 'HghPric', 'LwPric', 'ClsPric', 'LastPric',
                'PrvsClsgPric', 'TtlTradgVol', 'TtlTrfVal', 'TtlNbOfTxsExctd']

bhavcopy_new = ['TIMESTAMP', 'ISIN', 'SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE',
                'TOTTRDQTY', 'TOTTRDVAL', 'TOTALTRADES']

future_price_volume_data_column = ['TIMESTAMP', 'INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PRICE', 'OPTION_TYPE', 'MARKET_TYPE',
                                   'OPENING_PRICE', 'TRADE_HIGH_PRICE', 'TRADE_LOW_PRICE', 'CLOSING_PRICE',
                                   'LAST_TRADED_PRICE', 'PREV_CLS', 'SETTLE_PRICE', 'TOT_TRADED_QTY', 'TOT_TRADED_VAL',
                                   'OPEN_INT', 'CHANGE_IN_OI', 'MARKET_LOT', 'UNDERLYING_VALUE']

india_vix_data_column = ['TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'CLOSE_INDEX_VAL', 'HIGH_INDEX_VAL',
                         'LOW_INDEX_VAL', 'PREV_CLOSE', 'VIX_PTS_CHG', 'VIX_PERC_CHG']

index_data_columns = ['TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'HIGH_INDEX_VAL', 'CLOSE_INDEX_VAL',
                      'LOW_INDEX_VAL', 'TRADED_QTY', 'TURN_OVER']

header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1",
    "Accept": "*/*",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
}

bhav_copy_Column_list = [
    "TradDt",
    "BizDt",
    "Sgmt",
    "Src",
    "FinInstrmTp",
    "FinInstrmId",
    "ISIN",
    "TckrSymb",
    "SctySrs",
    "XpryDt",
    "FininstrmActlXpryDt",
    "StrkPric",
    "OptnTp",
    "FinInstrmNm",
    "OpnPric",
    "HghPric",
    "LwPric",
    "ClsPric",
    "LastPric",
    "PrvsClsgPric",
    "UndrlygPric",
    "SttlmPric",
    "OpnIntrst",
    "ChngInOpnIntrst",
    "TtlTradgVol",
    "TtlTrfVal",
    "TtlNbOfTxsExctd",
    "SsnId",
    "NewBrdLotQty",
    "Rmks",
    "Rsvd1",
    "Rsvd2",
    "Rsvd3",
    "Rsvd4",
]

company_financial_Column_list = [
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


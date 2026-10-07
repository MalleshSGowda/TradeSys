from util.util import *


var_engine = get_engine("localhost", "src_db", "root", "root")

table_name = "yfinance_stock_major_holders"
table_name_1 = "yfinance_stock_institutional_holders"

truncate_table(table_name, var_engine)

tick = "ABAN.NS"

query = """SELECT distinct ticker FROM trading.stock order by ticker asc; """

# Create a connection and execute the query
with var_engine.connect() as conn:
    result = conn.execute(text(query))

    # Iterate over the results and print each SYMBOL
    for row in result:
        print(f"SYMBOL: {row[0]}")
        # Define the symbol of the company for which you want to fetch data
        tick = (
            row[0] + ".NS"
        )  # IDFC First Bank IDFCFIRSTB  ITALIANE 3IINFOTECH AGRITECH 5PAISA

        try:
            yf_tkr_obj = get_yfinance_ticker_obj(tick)

            stock_data_history = yf_tkr_obj.major_holders
            stock_data_history["date_created"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            stock_data_history["symbol_name"] = row[0]  # main_symbol

            stock_data_history_1 = yf_tkr_obj.institutional_holders
            stock_data_history_1["date_created"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            stock_data_history_1["symbol_name"] = row[0]  # main_symbol

            if not stock_data_history.empty:
                write_to_mysql(
                    stock_data_history, table_name, var_engine, "append", True
                )

                write_to_mysql(
                    stock_data_history_1, table_name_1, var_engine, "append", True
                )

            else:
                print(f"No data for company financial {tick}")

        except Exception as e:
            print(f"Error getting company financial details for {tick}: {e}")

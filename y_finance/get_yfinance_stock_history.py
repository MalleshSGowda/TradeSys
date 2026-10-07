from util.util import *


var_engine = get_engine("localhost", "src_db", "root", "root")

table_name = "yfinance_stock_history"

truncate_table(table_name, var_engine)

tick = "AURDIS.NS"

query = """SELECT distinct ticker FROM trading.stock order by ticker asc limit 5; """

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

            stock_data_history = get_yfinance_ticker_history(yf_tkr_obj, "1mo")
            stock_data_history["date_created"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            stock_data_history["symbol_name"] = row[0]  # main_symbol

            if not stock_data_history.empty:
                write_to_mysql(
                    stock_data_history, table_name, var_engine, "append", True
                )

            else:
                print(f"No data for company financial {tick}")

        except Exception as e:
            print(f"Error getting company financial details for {tick}: {e}")

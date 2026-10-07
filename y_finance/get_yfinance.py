from util.column_list import info_column_list
from util.util import *

cnt = 1
var_engine = get_engine("localhost", "src_db", "root", "root")


table_name_his = "yfinance_stock_history"
table_name_com_fin = "yfinance_company_financial"
table_name_rec = "yfinance_stock_recommendations"
table_name_rec_sum = "yfinance_stock_recommendations_summary"
table_name_bal_sheet = "yfinance_stock_balance_sheet"
table_name_maj_hold = "yfinance_stock_major_holders"
table_name_inst_hold = "yfinance_stock_institutional_holders"


truncate_table(table_name_rec, var_engine)
truncate_table(table_name_rec_sum, var_engine)
truncate_table(table_name_his, var_engine)
truncate_table(table_name_bal_sheet, var_engine)
truncate_table(table_name_maj_hold, var_engine)
truncate_table(table_name_inst_hold, var_engine)
truncate_table(table_name_com_fin, var_engine)


tick = "0P0000XW8P.BO"

query = """SELECT  ticker,ROW_NUMBER() OVER (ORDER BY ticker ASC) AS id FROM trading.stock GROUP BY ticker ORDER BY 2 desc; """

try:

    # Create a connection and execute the query
    with var_engine.connect() as conn:
        result = conn.execute(text(query))

        # Iterate over the results and print each SYMBOL
        for row in result:
            print(f"SYMBOL: {row[0]} : {row[1]}")

            # Define the symbol of the company for which you want to fetch data
            tick = (
                row[0] + ".NS"
            )  # IDFC First Bank IDFCFIRSTB  ITALIANE 3IINFOTECH AGRITECH 5PAISA

            try:
                yf_tkr_obj = get_yfinance_ticker_obj(tick)

                try:
                    # stock_history = get_yfinance_ticker_history(yf_tkr_obj, "max")

                    stock_history = get_yfinance_ticker_history_period_interval(
                        yf_tkr_obj, "1d", "max"
                    )

                    stock_history["date_created"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    stock_history["symbol_name"] = row[0]  # main_symbol

                    stock_history = stock_history.drop(
                        "Capital Gains", axis=1, errors="ignore"
                    )
                    if not stock_history.empty:
                        write_to_mysql(
                            stock_history, table_name_his, var_engine, "append", True
                        )

                except Exception as e:
                    print(f"Error in Stock history : {e}")
                    error_log(row[0], e, var_engine)

                try:
                    # Get the company's info
                    info = yf_tkr_obj.info

                    # Convert the info dictionary to a DataFrame
                    df = pd.DataFrame([info])
                    dfa = pd.DataFrame()

                    for col in df.columns:
                        if col in info_column_list:
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

                    dfa.to_sql(
                        name=table_name_com_fin,
                        con=var_engine,
                        if_exists="append",
                        index=False,
                    )
                except Exception as e:
                    error_log(row[0], e, var_engine)
                    print(f"Error in Company financial : {e}")

                try:

                    stock_recom = yf_tkr_obj.recommendations
                    stock_recom["date_created"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    stock_recom["symbol_name"] = row[0]  # main_symbol
                    if not stock_recom.empty:
                        write_to_mysql(
                            stock_recom, table_name_rec, var_engine, "append", True
                        )

                except Exception as e:
                    print(f"Error in Stock recommandation : {e}")
                    error_log(row[0], e, var_engine)

                try:
                    stock_recom_sum = yf_tkr_obj.recommendations_summary
                    stock_recom_sum["date_created"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    stock_recom_sum["symbol_name"] = row[0]  # main_symbol
                    if not stock_recom_sum.empty:
                        write_to_mysql(
                            stock_recom_sum,
                            table_name_rec_sum,
                            var_engine,
                            "append",
                            True,
                        )
                except Exception as e:
                    print(f"Error in Stock recommandation summary : {e}")
                    error_log(row[0], e, var_engine)

                try:

                    stock_major_holder = yf_tkr_obj.major_holders
                    stock_major_holder["date_created"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    stock_major_holder["symbol_name"] = row[0]  # main_symbol
                    if not stock_major_holder.empty:
                        write_to_mysql(
                            stock_major_holder,
                            table_name_maj_hold,
                            var_engine,
                            "append",
                            True,
                        )

                except Exception as e:
                    print(f"Error in Stock major holder : {e}")
                    error_log(row[0], e, var_engine)

                try:

                    stock_inst_holder = yf_tkr_obj.institutional_holders
                    stock_inst_holder["date_created"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    stock_inst_holder["symbol_name"] = row[0]  # main_symbol
                    if not stock_inst_holder.empty:
                        write_to_mysql(
                            stock_inst_holder,
                            table_name_inst_hold,
                            var_engine,
                            "append",
                            True,
                        )
                except Exception as e:
                    print(f"Error in Stock institutional holder : {e}")
                    error_log(row[0], e, var_engine)

                try:
                    stock_bal_sheet = yf_tkr_obj.balance_sheet
                    stock_bal_sheet["date_created"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    stock_bal_sheet["symbol_name"] = row[0]  # main_symbol

                    if not stock_bal_sheet.empty:
                        write_to_mysql(
                            stock_bal_sheet,
                            table_name_bal_sheet,
                            var_engine,
                            "append",
                            True,
                        )
                except Exception as e:
                    print(f"Error in Balance sheet : {e}")
                    error_log(row[0], e, var_engine)

            except Exception as e:
                print(f"Error getting ticker  {tick}: {e}")
                error_log("Ticker", e, var_engine)
except Exception as e:
    print(f"Error getting ticker  {tick}: {e}")
    error_log("Main", e, var_engine)

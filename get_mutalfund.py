import yfinance as yf
import pandas as pd
from util.util import *
from util.util_mutalfund import *
from sqlalchemy.exc import SQLAlchemyError
import time

mutual_fund_code = "1521670000"

var_engine = get_engine("localhost", "source_db", "root", "root")

mutual_fund_list_table = "mutual_fund_list"
mutual_fund_nav_present_table = "mutual_fund_nav_present"
mutual_fund_nav_history_table = "mutual_fund_nav_history"
# mutual_fund_nav_history_table_tp1 = "mutual_fund_nav_history_tp1"
# mutual_fund_nav_history_table_tp2 = "mutual_fund_nav_history_tp2"
# mutual_fund_nav_history_table_tp3 = "mutual_fund_nav_history_tp3"

truncate_table(mutual_fund_list_table, var_engine)
truncate_table(mutual_fund_nav_present_table, var_engine)
truncate_table(mutual_fund_nav_history_table, var_engine)
# truncate_table(mutual_fund_nav_history_table_tp1, var_engine)
# truncate_table(mutual_fund_nav_history_table_tp2, var_engine)
# truncate_table(mutual_fund_nav_history_table_tp3, var_engine)

mutual_fund_list = get_all_mutalfund_details()
write_to_mysql(mutual_fund_list, mutual_fund_list_table, var_engine, "append", False)

mutual_fund_nav_present = get_mutalfund_present_nav_all()
write_to_mysql(
    mutual_fund_nav_present, mutual_fund_nav_present_table, var_engine, "append", False
)

exit()

df_mutual_fund_list = mutual_fund_nav_present[
    (mutual_fund_nav_present["date_nav_id"] > "20241101")
    & (mutual_fund_nav_present["scheme_code"] > "132995")
].sort_values(by="scheme_code", ascending=True)

i = 0
for index, row in df_mutual_fund_list.iterrows():
    print(row["scheme_code"])
    mutual_fund_code = row["scheme_code"]

    if mutual_fund_code != "Code":
        mutual_fund_details = get_mutal_fund_nav_history_from_dt(
            mutual_fund_code, "20241101"
        )
        write_to_mysql(
            mutual_fund_details,
            mutual_fund_nav_history_table,
            var_engine,
            "append",
            False,
        )

    if i < 100000:
        i = i + 1
        print(i, mutual_fund_code)
        # if (i % 100) == 0:
        #    time.sleep(300)

    else:
        exit()

exit()


# df = get_all_mutal_fund_search("HDFC Mid-Cap Opportunities Fund - Growth Option - Direct Plan")
# print(df)

start_date = pd.to_datetime("01-11-2024", format="%d-%m-%Y")
end_date = pd.to_datetime("30-11-2024", format="%d-%m-%Y")

exit()

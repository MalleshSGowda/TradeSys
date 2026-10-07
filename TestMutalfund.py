import yfinance as yf
import pandas as pd
from util.util_mutalfund import *
from util.util import *
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from mftool import Mftool

mutual_fund_code = "152167"


mf_obj = Mftool()

var_engine = get_engine("localhost", "src_db", "root", "root")

mutual_fund_list_table = "mutual_fund_list"
mutual_fund_details_table = "mutual_fund_details"
mutual_fund_nav_history_table = "mutual_fund_nav_history"
mutual_fund_nav_present_table = "mutual_fund_nav_present"

truncate_table(mutual_fund_list_table, var_engine)
truncate_table(mutual_fund_details_table, var_engine)
truncate_table(mutual_fund_nav_history_table, var_engine)
truncate_table(mutual_fund_nav_present_table, var_engine)


mutual_fund_list = get_all_mutal_fund_list(mf_obj)
## print(mutual_fund_list)
write_to_mysql(mutual_fund_list, mutual_fund_list_table, var_engine, "append", False)

print(mf_obj.get_scheme_quote(100124))

print("#############3")

exit()
i = 0
for index, row in mutual_fund_list.iterrows():
    # print(row["Key"])
    mutual_fund_code = row["Key"]

    if mutual_fund_code != "Scheme Code":
        print(mf_obj.get_scheme_quote(mutual_fund_code))

        # mutual_fund_nav_present = get_mutual_fund_Nav_updated_on(mf_obj, mutual_fund_code)
        # write_to_mysql(mutual_fund_nav_present,mutual_fund_nav_present_table,var_engine,"append",False)

        # mutual_fund_nav_history = get_mutual_fund_Nav_history(mf_obj, mutual_fund_code)
        # write_to_mysql(mutual_fund_nav_history,mutual_fund_nav_history_table,var_engine,"append",False)


exit()


# df = get_all_mutal_fund_search("HDFC Mid-Cap Opportunities Fund - Growth Option - Direct Plan")
# print(df)


df = get_mutual_fund_Nav_updated_on(mf_obj, mutual_fund_code)
print(df)

start_date = pd.to_datetime("01-11-2024", format="%d-%m-%Y")
end_date = pd.to_datetime("30-11-2024", format="%d-%m-%Y")

df = get_mutual_fund_Nav_history_for_period(
    mf_obj, mutual_fund_code, start_date, end_date
)
print(df)


exit()

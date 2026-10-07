# Import modules
import pandas as pd
import requests
import csv
import zipfile
from io import BytesIO, StringIO
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from util.constants import *


def get_dataframe_values(dataframe, Column_list):
    dfa = pd.DataFrame()
    try:

        # Convert any complex types (like dictionaries) to strings
        for col in dataframe.columns:
            if col in Column_list:
                if isinstance(dataframe[col].iloc[0], (dict, list)):
                    dataframe[col] = dataframe[col].apply(lambda x: str(x))
                    dfa[col] = dataframe[col].apply(lambda x: str(x))
                else:
                    # print(f" ** {col} : {df[col].values}")
                    dfa[col] = dataframe[col]

    except Exception as e:
        print(f"Failed to get values for dataframe columns values {e}")
    return dfa


# Create mysql engine
def get_engine(
    host="localhost",
    database="your_database",
    user="your_username",
    password="your_password",
):

    try:
        db_url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
        print(f"MySql Engine created")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
    return engine


# Function to truncate the table
def truncate_table(table_name="table_name", engine="engine"):
    try:
        # engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(f"TRUNCATE TABLE {table_name}"))
                print(f"Table {table_name} has been truncated.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


# Function to error log table
def error_log(info="ticker", description="description", engine="engine"):
    try:

        with engine.connect() as connection:
            with connection.begin():
                connection.execute(
                    text(
                        f"insert into src_db.error_log(info,description)values('{info}','{description}')"
                    )
                )
                # connection.execute(text(f"insert into error_log(info,description)values("{info}","{description}")"));
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


#  function dataframe to mysql table
def write_to_mysql(
    data_df,
    table_name="table_name",
    engine="engine",
    table_exits="append",
    index_val=True,
):
    # engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    try:
        data_df.to_sql(
            name=table_name, con=engine, if_exists=table_exits, index=index_val
        )
        # print("Data successfully written to MySQL.")
        # error_log(table_name, "Data Insert successfully", engine)

    except Exception as e:
        print(f"Error writing data to MySQL: {e}")
        error_log(table_name, e, engine)
        return "Failed"
    return "Successfull"


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

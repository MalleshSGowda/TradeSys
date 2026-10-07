import mysql.connector
from datetime import datetime, timedelta

# Establish a database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="trading_schema"
)


cursor = db.cursor()

# Define the start and end dates for the dimension table
start_date = datetime(2005, 1, 1)
end_date = datetime(2030, 12, 31)

current_date = start_date

# Function to check if a date is a weekend
def is_weekend(date):
    return date.weekday() >= 5

# Function to get the day of the week as a string
def get_day_of_week(date):
    return date.strftime('%A')

# Function to get the month name as a string
def get_month_name(date):
    return date.strftime('%B')

# Populate the date_dimension table
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    date_id = int(current_date.strftime('%Y%m%d'))
    year = current_date.year
    quarter = (current_date.month - 1) // 3 + 1
    month = current_date.month
    day = current_date.day
    week = current_date.isocalendar()[1]
    day_of_week = get_day_of_week(current_date)
    month_name = get_month_name(current_date)
    weekend = is_weekend(current_date)
    
    # Insert the date record into the date_dimension table
    cursor.execute("""
        INSERT INTO date_dimension (date_id,date, year, quarter, month, day, week, day_of_week, month_name, is_weekend)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (date_id, date_str, year, quarter, month, day, week, day_of_week, month_name, weekend))
    
    current_date += timedelta(days=1)

# Commit the transaction
db.commit()

# Close the cursor and connection
cursor.close()
db.close()

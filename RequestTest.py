from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up Selenium WebDriver (use your path to chromedriver)
driver = webdriver.Chrome(executable_path="path/to/chromedriver")

# URL to scrape
url = "file:///C:/Users/MalleshPC/workspace/workspace_trade/nse_bulk_deals.html"

# Open the page
driver.get(url)

# Wait for the page to load completely
time.sleep(10)

# Locate the table (use the appropriate class or ID for the table)
try:
    # Replace 'table-selector' with the appropriate CSS selector for the table
    table = driver.find_element(By.XPATH, "//table")

    # Extract table rows
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []

    # Loop through each row and extract cell data
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])

    # Convert to a DataFrame for easy handling
    columns = [header.text for header in table.find_elements(By.TAG_NAME, "th")]
    df = pd.DataFrame(data, columns=columns)

    # Save the data to a CSV file
    df.to_csv("nse_bulk_and_block_deals.csv", index=False)
    print("Data saved successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
driver.quit()

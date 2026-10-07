from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL of the best mutual funds (10-year return period)
url = "https://www.valueresearchonline.com/funds/best-mutual-funds/?return-period=10Y&plan-type=1"


# Function to scrape mutual fund data using Selenium
def scrape_mf_data_selenium(url):
    # Set up the Chrome WebDriver (automatically manage ChromeDriver)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)

    # Initialize driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # Open the URL
    driver.get(url)

    # Wait for the table to load (add an explicit wait)
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "table datatable-fixedheader portfolio-table dataTable no-footer",
                )
            )
        )
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Loop through each row and extract data
        for row in rows[1:]:  # Skipping the header row
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 1:
                fund_name = cols[0].text.strip()
                one_year_return = cols[1].text.strip()
                three_year_return = cols[2].text.strip()
                five_year_return = cols[3].text.strip()
                ten_year_return = cols[4].text.strip()
                expense_ratio = cols[5].text.strip()

                # Print the extracted data
                print(f"Fund Name: {fund_name}")
                print(f"1 Year Return: {one_year_return}")
                print(f"3 Year Return: {three_year_return}")
                print(f"5 Year Return: {five_year_return}")
                print(f"10 Year Return: {ten_year_return}")
                print(f"Expense Ratio: {expense_ratio}")
                print("-" * 50)
    except Exception as e:
        print(f"Error while scraping: {e}")
    finally:
        # Close the browser after scraping
        driver.quit()


# Call the Selenium-based function
scrape_mf_data_selenium(url)

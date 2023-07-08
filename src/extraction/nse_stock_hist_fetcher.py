import os
import datetime
import logging
import requests
import pandas as pd
from requests_html import HTMLSession
from nse_data_fetcher import get_cookie_value
from nse_data_fetcher import is_holiday
from nse_data_fetcher import download_csv_file
from nse_data_fetcher import save_to_csv

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
NSE_URL = 'https://www.nseindia.com'
HOLIDAY_DATA_PATH = 'data/raw/holiday_data/trading_holiday.csv'
FULL_BHAVDATA_PATH = 'data/raw/sec_bhavdata_full/'
MA_REPORT_PATH = 'data/raw/ma_report/'

# Specify the dates for download the file
# Use %d-%b-%Y format will specifying the date
START_DATE = '01-Apr-2023'
END_DATE = datetime.datetime.now().strftime('%d-%b-%Y')

def main():
    """
    This is the main function that orchestrates the execution of the script.
    It initializes the `HTMLSession` object, retrieves the cookie value,
    download the sector full bhavdata from specified data
    saves it to a CSV file, and downloads two other CSV files.
    """

    # Initialize session
    session = HTMLSession()

    # Get cookie value
    cookie_value = get_cookie_value(session)

    # Set headers
    headers = {
        'Referer': NSE_URL,
        'Cookie': f'cookie_name={cookie_value}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # Convert start and end dates to datetime objects
    start_date = datetime.datetime.strptime(START_DATE, "%d-%b-%Y")
    end_date = datetime.datetime.strptime(END_DATE, "%d-%b-%Y")

    download_date = start_date
    one_day = datetime.timedelta(days=1)

    while download_date <= end_date:

        # Check if it's an holiday
        if is_holiday(download_date.strftime('%d-%b-%Y')):
            logging.info(f"Skipping download for holiday: {download_date}")
        else:
        # Get file download date
            current_date_full_bhavdata = download_date.strftime("%d-%m-%Y").replace("-", "")
            current_date_ma_report = download_date.strftime("%d-%m-%y").replace("-", "")

            # Download the CSV file of security-wise full bhavcopy
            full_bhavdata_file_url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{current_date_full_bhavdata}.csv"
            download_csv_file(session, full_bhavdata_file_url, FULL_BHAVDATA_PATH)
            print(f"Security-wise full bhavdata downloaded successfully for date {download_date}")

            # Download the Market Activity report CSV file
            ma_report_file_url = f'https://archives.nseindia.com/archives/equities/mkt/MA{current_date_ma_report}.csv'
            download_csv_file(session, ma_report_file_url,MA_REPORT_PATH)
            print(f'MA report downloaded successfully for date {download_date}')

        # Move to the next date
        download_date += one_day
    

if __name__ == "__main__":
    main()


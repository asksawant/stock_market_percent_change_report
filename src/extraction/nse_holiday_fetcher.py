import logging
import requests
import pandas as pd
from requests_html import HTMLSession
import os
import datetime
from nse_data_fetcher import get_cookie_value 
 
# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_trading_holiday_data():

    session = HTMLSession()
    cookie_value = get_cookie_value(session)

    headers = {
        'Referer': 'https://www.nseindia.com',
        'Cookie': f'cookie_name={cookie_value}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    trading_holiday_url = 'https://www.nseindia.com/api/holiday-master?type=trading'
    response = session.get(trading_holiday_url)

    if response.status_code == 200:
        data = response.json().get('CM', [])
        df = pd.DataFrame(data, columns=['tradingDate'])
        df = df.rename(columns={'tradingDate': 'HolidayDate'})
        df['HolidayDate'] = df['HolidayDate'].str.strip()
        df['HolidayDate'] = pd.to_datetime(df['HolidayDate'], format='%d-%b-%Y')
        # print(df.head())
        current_year = datetime.datetime.now().year
        saturdays = pd.date_range(start=f'01-Jan-{current_year}', end=f'31-Dec-{current_year}', freq='W-SAT')
        sundays = pd.date_range(start=f'01-Jan-{current_year}', end=f'31-Dec-{current_year}', freq='W-SUN')

        saturdays_df = pd.DataFrame({'HolidayDate': saturdays})
        sundays_df = pd.DataFrame({'HolidayDate': sundays})

        df = pd.concat([df, saturdays_df, sundays_df], ignore_index=True)
        df['HolidayDate'] = df['HolidayDate'].dt.strftime('%d-%b-%Y')

        csv_file = 'data/raw/holiday_data/trading_holiday.csv'
        df.to_csv(csv_file, index=False)
        print(f"Trading holiday data saved to {csv_file}")
        logging.info(f"Trading holiday data saved to {csv_file}")
    else:
        logging.warning(f"Failed to fetch trading holiday data.")

if __name__ == '__main__':
    fetch_trading_holiday_data()

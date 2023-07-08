import os
import datetime
import logging
import requests
import pandas as pd
from requests_html import HTMLSession

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
NSE_URL = 'https://www.nseindia.com'
COMBINED_DATA_PATH = 'data/raw/sector_list/'
HOLIDAY_DATA_PATH = 'data/raw/holiday_data/trading_holiday.csv'
FULL_BHAVDATA_PATH = 'data/raw/sec_bhavdata_full/'
MA_REPORT_PATH = 'data/raw/ma_report/'

# # Variables
# TODAY = datetime.datetime.now().strftime('%d-%b-%Y')

SECTOR_INDEX = {
    'NIFTY 50' : 'NIFTY%2050',
    'NIFTY NEXT 50' : 'NIFTY%20NEXT%2050',
    'NIFTY MIDCAP 50' : 'NIFTY%20MIDCAP%2050',
    'NIFTY AUTO' : 'NIFTY%20AUTO',
    'NIFTY BANK' : 'NIFTY%20BANK',
    'NIFTY ENERGY' : 'NIFTY%20ENERGY',
    'NIFTY FIN SERVICE' : 'NIFTY%20FINANCIAL%20SERVICES',
    'NIFTY FMCG' : 'NIFTY%20FMCG',
    'NIFTY IT' : 'NIFTY%20IT',
    'NIFTY MEDIA' : 'NIFTY%20MEDIA',
    'NIFTY METAL' : 'NIFTY%20METAL',
    'NIFTY PHARMA': 'NIFTY%20PHARMA',
    'NIFTY PSU BANK' : 'NIFTY%20PSU%20BANK',
    'NIFTY REALTY' : 'NIFTY%20REALTY',
    'NIFTY PVT BANK' : 'NIFTY%20PRIVATE%20BANK',
    'NIFTY HEALTHCARE' : 'NIFTY%20HEALTHCARE%20INDEX',
    'NIFTY CONSR DURBL' : 'NIFTY%20CONSUMER%20DURABLES',
    'NIFTY OIL AND GAS' : 'NIFTY%20OIL%20%26%20GAS',
    'NIFTY COMMODITIES' : 'NIFTY%20COMMODITIES',
    'NIFTY CONSUMPTION' : 'NIFTY%20INDIA%20CONSUMPTION',
    'NIFTY CPSE' : 'NIFTY%20CPSE',
    'NIFTY INFRA' : 'NIFTY%20INFRASTRUCTURE',
    'NIFTY MNC' : 'NIFTY%20MNC',
    'NIFTY PSE' : 'NIFTY%20PSE',
    'NIFTY SERV SECTOR' : 'NIFTY%20SERVICES%20SECTOR'
}

def get_cookie_value(session):
    """
    This function takes an HTMLSession object as input and sends a
    GET request to 'https://www.nseindia.com'to retrieve a cookie value.
    It returns the value of the cookie named 'cookie_name'.
    """
    response = session.get(NSE_URL)
    return session.cookies.get('cookie_name')

def is_holiday(date):
    """
    This function checks if a given date is a holiday by 
    reading a CSV file containing trading holiday data.
    It returns a boolean value indicating whether the date is a holiday.
    """

    holiday_df = pd.read_csv(HOLIDAY_DATA_PATH)
    return date in holiday_df.values

def get_previous_trading_day():
    """
    This function calculates the previous trading day.
    It returns the previous trading day as a string in the format '%d-%b-%Y'.
    """

    # current_date = datetime.datetime(2023, 7, 2, 6, 33, 27, 873002)
    current_date = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    previous_day = current_date - one_day

    while is_holiday(previous_day.strftime('%d-%b-%Y')):
        previous_day -= one_day
    
    return previous_day.strftime('%d-%b-%Y')

def fetch_sector_data(session, sector_name, sector_index_value, date):
    """
    This function fetches sector data by sending a GET request to the NSE API.
    It takes an `HTMLSession` object, sector name, and sector index value as inputs.
    It returns a Pandas DataFrame containing the fetched data for the sector.
    """

    sector_live_data_url = f'{NSE_URL}/api/equity-stockIndices?index={sector_index_value}'
    response = session.get(sector_live_data_url)

    if response.status_code == 200:
        data = response.json().get('data', [])
        df = pd.DataFrame(data, columns=['priority', 'symbol'])
        df = df.rename(columns={'symbol': 'SYMBOL'})
        df = df[df['priority'] != 1].drop('priority', axis=1)
        df['SECTOR'] = sector_name
        logging.info(f"Fetched data for {sector_name} for date {date}")
        return df
    else:
        logging.warning(f"Failed to fetch data for {sector_name} for date {date}")
        csv_file = COMBINED_DATA_PATH
        try:
            df = pd.read_csv(csv_file)
            logging.info(f"Using data from {csv_file} for {sector_name}")
            df['SECTOR'] = sector_name
            return df
        except FileNotFoundError:
            logging.warning(f"CSV file not found for {sector_name}")
            return pd.DataFrame()
        
def combine_sector_data(sector_data):
    """
    This function combines a list of sector data DataFrames into a single DataFrame.
    It takes a list of sector data DataFrames as input and returns the combined DataFrame.
    """

    return pd.concat(sector_data, ignore_index=True)

def save_to_csv(df, filename, folder_path):
    """
    This function saves a DataFrame to a CSV file.
    It takes a DataFrame, filename, and folder path as inputs
    and writes the DataFrame to the specified CSV file.
    """

    file_path = folder_path + filename
    df.to_csv(file_path, index=False)
    logging.info(f"Saved data to {file_path}")

def download_csv_file(session, file_url, folder_path):
    """
    This function downloads a CSV file from a given URL using an `HTMLSession` object.
    It takes the session object, file URL, and folder path as inputs 
    and saves the downloaded file to the specified folder.

    """
    response = session.get(file_url)
    file_name = response.url[file_url.rfind('/')+1:]
    file_path = os.path.join(folder_path, file_name)

    if response.status_code == 200:
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        # Save the file
        with open(file_path, "wb") as file:
            file.write(response.content)
        logging.info(f"File downloaded successfully: {file_path}")
    else:
        logging.warning(f"Failed to download the file : {file_path}")
    
def main():
    """
    This is the main function that orchestrates the execution of the script.
    It initializes the `HTMLSession` object, retrieves the cookie value,
    checks if it's a holiday, fetches sector data, combines the data,
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

    # Check if today is a holiday
    # today = '03-Jul-2023'
    today = datetime.datetime.now().strftime('%d-%b-%Y')

    # Fetch sector data
    sector_data = []
    for sector_name, sector_index_value in SECTOR_INDEX.items():
        logging.info(f"Fetching data for {sector_name}...")
        data = fetch_sector_data(session, sector_name, sector_index_value, today)
        sector_data.append(data)
    
    # Combine sector data
    combined_df = combine_sector_data(sector_data)

    # Save combined data to CSV
    save_to_csv(combined_df, 'combined_data.csv', COMBINED_DATA_PATH)
    print("Successfully saved the sector - stocks list")

    if is_holiday(today):
        logging.info("Today is a trading holiday. No data will be fetched.")
        print('Today is trading holiday, no data will be fetched')
        return
    
    # Get today's date
    current_date_full_bhavdata = datetime.datetime.now().strftime('%d%m%Y')
    current_date_ma_report = datetime.datetime.now().strftime('%d%m%y')

    # Download the CSV file of security-wise full bhavcopy
    full_bhavdata_file_url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{current_date_full_bhavdata}.csv"
    download_csv_file(session, full_bhavdata_file_url, FULL_BHAVDATA_PATH)
    print(f"Security-wise full bhavdata downloaded successfully")

    # Download the Market Activity report CSV file
    ma_report_file_url = f'https://archives.nseindia.com/archives/equities/mkt/MA{current_date_ma_report}.csv'
    download_csv_file(session, ma_report_file_url,MA_REPORT_PATH)
    print(f'MA report downloaded successfully')

    # Getting data for previous day
    previous_trading_day = get_previous_trading_day()
    previous_date_full_bhavdata = pd.to_datetime(previous_trading_day).strftime("%d-%m-%Y").replace("-", "")
    previous_date_ma_report = pd.to_datetime(previous_trading_day).strftime("%d-%m-%y").replace("-", "")

    # Download the CSV file of security-wise full bhavcopy for previous trading day
    full_bhavdata_file_url_previous_day = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{previous_date_full_bhavdata}.csv"
    download_csv_file(session, full_bhavdata_file_url_previous_day, FULL_BHAVDATA_PATH)
    print("Successfully downloaded previous trading day's security-wise full bhavdata")

    # Download the Market Activity report CSV file for previous trading day
    ma_report_file_url_previous_day = f'https://archives.nseindia.com/archives/equities/mkt/MA{previous_date_ma_report}.csv'
    download_csv_file(session, ma_report_file_url_previous_day, MA_REPORT_PATH)
    print("Successfully downloaded previous trading day's MA report")


if __name__ == "__main__":
    main()
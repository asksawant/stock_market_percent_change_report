import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(filename='logs/data_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BHAVDATA_FOLDER_PATH = 'data/raw/sec_bhavdata_full/'
MA_REPORT_FOLDER_PATH = 'data/raw/ma_report/'
STAGING_FOLDER_PATH = 'data/interim/'
PROCESSED_FOLDER_PATH = 'data/processed/'
SECTOR_LIST_FILE_PATH = 'data/raw/sector_list/combined_data.csv'
HOLIDAY_DATA_PATH = 'data/raw/holiday_data/trading_holiday.csv'

# Function to clean Bhavdata files
def clean_bhavdata_files():
    try:
        # Get a list of all CSV files in the folder
        full_bhavdata_csv_files = [file for file in os.listdir(BHAVDATA_FOLDER_PATH) if file.endswith('.csv')]

        # Initialize an empty list to store the data frames
        bhavdata_df_list = []

        # Read each CSV file and append its data frame to the list
        for file in full_bhavdata_csv_files:
            file_path = os.path.join(BHAVDATA_FOLDER_PATH, file)
            dfs = pd.read_csv(file_path)
            bhavdata_df_list.append(dfs)

        # Concatenate the data frames into a single data frame
        bhavdata_df = pd.concat(bhavdata_df_list, ignore_index=True)

        # Data cleaning operations
        bhavdata_df = bhavdata_df.rename(columns=lambda x: x.strip())
        bhavdata_df = bhavdata_df.rename(columns={'DATE1': 'DATE'})
        bhavdata_df['SERIES'] = bhavdata_df['SERIES'].str.strip()
        bhavdata_df['DATE'] = bhavdata_df['DATE'].str.strip()
        bhavdata_df = bhavdata_df[bhavdata_df['SERIES'] == 'EQ']
        bhavdata_df = bhavdata_df.drop(columns=['SERIES', 'PREV_CLOSE', 'AVG_PRICE', 'TURNOVER_LACS', 'DELIV_PER'], axis=1)
        bhavdata_df['LAST_PRICE'] = bhavdata_df['LAST_PRICE'].astype(float)
        bhavdata_df['DELIV_QTY'] = bhavdata_df['DELIV_QTY'].astype(int)
        bhavdata_df['DATE'] = pd.to_datetime(bhavdata_df['DATE'])

        # Save cleaned Bhavdata to staging folder
        bhavdata_df.to_csv(os.path.join(STAGING_FOLDER_PATH, 'sec_bhavdata_full_combined.csv'), index=False)

        logging.info('Bhavdata cleaning completed.')

        # Save the fact bhavdata
        fact_daily_bhavdata_df = bhavdata_df.copy()
        # Read the sector list file
        sector_list_df = pd.read_csv(SECTOR_LIST_FILE_PATH)

        # Selecting only NIFTY 50, Next 50 and Midcap 50 stocks
        sector_list_df = sector_list_df[sector_list_df['SECTOR'].isin(['NIFTY 50','NIFTY NEXT 50','NIFTY MIDCAP 50'])]

        # Filter the symbols based on those present in the sector list
        symbols_in_sector_list = sector_list_df['SYMBOL'].unique()
        fact_daily_bhavdata_df = fact_daily_bhavdata_df[fact_daily_bhavdata_df['SYMBOL'].isin(symbols_in_sector_list)]

        # Join with sector_list_df to add sector name
        fact_daily_bhavdata_df = pd.merge(fact_daily_bhavdata_df, sector_list_df[['SYMBOL', 'SECTOR']], on='SYMBOL', how='left')

        fact_daily_bhavdata_df.reset_index(drop =True, inplace=True)
        fact_daily_bhavdata_df.reset_index(inplace=True)
        fact_daily_bhavdata_df.rename(columns={'index': 'ID_BHAV'}, inplace=True)
        fact_daily_bhavdata_df = fact_daily_bhavdata_df[['ID_BHAV','SYMBOL', 'SECTOR' , 'DATE', 'LAST_PRICE',]]
        fact_daily_bhavdata_df.to_csv(os.path.join(PROCESSED_FOLDER_PATH, 'fact_bhavdata.csv'), index=False)

        logging.info('Daily Bhavdata Fact file saved')

        return bhavdata_df
    except Exception as e:

        logging.error(f'Error in cleaning Bhavdata files: {str(e)}')

# Function to clean MA Report files
def clean_ma_report_files():
    try:
        # Get a list of all CSV files in the folder
        ma_report_csv_files = [file for file in os.listdir(MA_REPORT_FOLDER_PATH) if file.endswith('.csv')]

        # Initialize an empty list to store the data frames
        ma_report_df_list = []

        # Iterate over each CSV file
        for file in ma_report_csv_files:
            file_path = os.path.join(MA_REPORT_FOLDER_PATH, file)

            # Extract the date from the file name
            date_str = file[2:-4]
            day = int(date_str[:2])
            month = int(date_str[2:4])
            year = 2000 + int(date_str[4:])

            # Read the CSV file and extract the desired data
            dfs = pd.read_csv(file_path, skiprows=8, usecols=range(1, 8), nrows=71)

            # Add the date column to the dataframe
            dfs['DATE'] = pd.to_datetime(f'{day}-{month}-{year}', format='%d-%m-%Y')

            # Append the extracted dataframe to the list
            ma_report_df_list.append(dfs)

        # Concatenate the data frames into a single data frame
        ma_report_df = pd.concat(ma_report_df_list, ignore_index=True)

        # Data cleaning operations
        ma_report_df['INDEX'] = ma_report_df['INDEX'].str.upper()
        ma_report_df = ma_report_df[['INDEX', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
        ma_report_df = ma_report_df.rename(columns={'INDEX': 'SECTOR'})

        # Save cleaned MA Report to staging folder
        ma_report_df.to_csv(os.path.join(STAGING_FOLDER_PATH, 'ma_report_combined.csv'), index=False)

        logging.info('MA Report cleaning completed.')

            # Save the fact bhavdata
        fact_ma_report_df = ma_report_df.copy()

        # Read the sector list file
        sector_list_df = pd.read_csv(SECTOR_LIST_FILE_PATH)

        # Filter the sectors based on those present in the sector list
        sectors_in_sector_list = sector_list_df['SECTOR'].unique()
        fact_ma_report_df = fact_ma_report_df[fact_ma_report_df['SECTOR'].isin(sectors_in_sector_list)]

        fact_ma_report_df.reset_index(drop=True, inplace=True)
        fact_ma_report_df.reset_index(inplace=True)
        fact_ma_report_df.rename(columns={'index': 'ID_MA'}, inplace=True)
        fact_ma_report_df = fact_ma_report_df[['ID_MA','SECTOR','DATE','CLOSE']]
        fact_ma_report_df.to_csv(os.path.join(PROCESSED_FOLDER_PATH, 'fact_MA_report.csv'), index=False)

        logging.info('MA report Fact file saved')

        return ma_report_df
    
    except Exception as e:

        logging.error(f'Error in cleaning MA Report files: {str(e)}')

# Function to create and save dimensions
def create_dimensions(bhavdata_df):

    try:
        # Read the sector list file
        sector_list_df = pd.read_csv(SECTOR_LIST_FILE_PATH)

        # Read trading holiday data
        holiday_df = pd.read_csv(HOLIDAY_DATA_PATH)

        # Create and save Dim_Datetime
        datetime_df = pd.DataFrame({'DATE': bhavdata_df['DATE'].unique()})
        datetime_df['DAY'] = datetime_df['DATE'].dt.day
        datetime_df['WEEKDAY'] = datetime_df['DATE'].dt.weekday
        datetime_df['WEEK'] = datetime_df['DATE'].dt.isocalendar().week
        datetime_df['MONTH'] = datetime_df['DATE'].dt.month
        datetime_df['QUARTER'] = datetime_df['DATE'].dt.quarter
        datetime_df['YEAR'] = datetime_df['DATE'].dt.year

        # Add FLAG column based on trading holidays
        datetime_df['FLAG'] = datetime_df['DATE'].isin(holiday_df['HolidayDate']).map({True: 'Holiday', False: 'Working'})

        datetime_df.reset_index(inplace=True)
        datetime_df.rename(columns={'index': 'ID_DATETIME'}, inplace=True)
        datetime_df.to_csv(os.path.join(PROCESSED_FOLDER_PATH, 'dim_datetime.csv'), index=False)

        logging.info('Dimensions created and saved.')
    
    except Exception as e:
    
        logging.error(f'Error in creating dimensions: {str(e)}')

def main():

    try:
        # Clean Bhavdata files
        bhavdata_df = clean_bhavdata_files()

        # Clean MA Report files
        ma_report_df = clean_ma_report_files()

        # Create and save dimensions
        create_dimensions(bhavdata_df)

        logging.info('Additional files created and saved.')

    except Exception as e:

        logging.error(f'Error in data processing: {str(e)}')



# Main script
if __name__ == '__main__':

    main()

import subprocess
import os
import logging

# Set up logging
log_file = 'logs/script_execution.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the paths to the scripts
NSE_DATA_FETCHER = "src/extraction/nse_data_fetcher.py"
DATA_PREPROCESSING = "src/integration/data_preprocessing.py"

def run_script(script_path):
    try:
        # Log a message to indicate the start of the script execution
        logging.info(f'Running script: {script_path}')

        # Run the script using subprocess
        subprocess.run(["python", script_path], check=True)

        # Log a message to indicate successful execution
        logging.info(f'Script execution completed: {script_path}')
    
    except subprocess.CalledProcessError as e:
        # Log the error message if the script execution fails
        logging.error(f'Script execution failed: {script_path} - {str(e)}')
    
    except Exception as e:
        # Log any other exceptions that occurred during execution
        logging.error(f'Error occurred during script execution: {script_path} - {str(e)}')

def main():

    try:
        # Define the paths to the scripts
        nse_data_fetcher_script = NSE_DATA_FETCHER
        data_preprocessing_script = DATA_PREPROCESSING

        # Run nse_data_fetcher.py
        run_script(nse_data_fetcher_script)

        # Run data-preprocessing.py
        run_script(data_preprocessing_script)

    except Exception as e:
        # Log any exceptions or errors that occurred during execution
        logging.error(f'Error occurred during script execution: {str(e)}')
    
if __name__ == '__main__':

    main()
    

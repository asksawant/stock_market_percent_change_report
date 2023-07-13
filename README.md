# Stock Market Percent Change Report

This repository contains the code and resources for generating a stock market percent change report using Python and Power BI.

## Power BI Report

The generated Power BI report provides insightful visualizations of the stock market percent change data. You can access the report using the following link:

[Power BI Report](https://app.powerbi.com/view?r=eyJrIjoiZTU5NGUyYmQtYWI4OS00OWVkLTg2Y2MtOTM3MmM5NzBiM2RjIiwidCI6IjU3OGQ5ZjNlLTlkMTItNDBiMi1hNjJlLWI3NzdiZGYyNTVhMiJ9)

## Description

The Stock Market Percent Change Report project retrieves stock market data from a reliable source, performs data preprocessing and analysis using Python, and visualizes the results using Power BI.

The project consists of the following components:
- `src/extraction/nse_data_fetcher.py`: Python script for fetching stock market data from the NSE (National Stock Exchange) website.
- `src/integration/data_preprocessing.py`: Python script for preprocessing the fetched data and generating necessary dimensions for analysis.
- `scripts/run_script.py`: Python script for executing the data extraction and data preprocessing scripts in sequence.
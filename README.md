Directory Structure
```
├── LICENSE
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── scripts                  <- Scripts directory for running Python scripts.
│   └── run_script.py      <- The Python script to be executed daily
│
├── src                <- Source code for use in this project.
│   │
│   ├── extraction           <- Scripts to download or generate data
│   │   ├── nse_data_fetcher.py
│   │   ├── nse_holiday_fetcher.py
│   │   ├── nse_stock_hist_fetcher.py
│   │
│   ├── integration       <- Scripts to turn raw data into features for modeling
│   │   └── data_preprocessing.py 
│   
├── reports  <- PowerBI pbix files
│   │   └── report_layout.pbix
│
└── ...
```

Power BI Dashboard Link
https://app.powerbi.com/view?r=eyJrIjoiMmI2YmY1YzYtMzg4Zi00YzJmLWIwY2ItNWIxMWNjNDdjNzkyIiwidCI6IjU3OGQ5ZjNlLTlkMTItNDBiMi1hNjJlLWI3NzdiZGYyNTVhMiJ9
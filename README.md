# Scraping CMA Typhoon Data

This repository contains a script to scrape typhoon data from the China Meteorological Administration (CMA) website. The script retrieves typhoon numbers and names for a given year and detailed information for a specific typhoon by its number. The data can be saved as CSV and Excel files.

## Features

- Retrieve typhoon numbers and names for a specified year
- Get detailed information for a specific typhoon
- Save typhoon data as CSV and Excel files

## Requirements
- Requests library
- Pandas library
- Openpyxl  library
  
You can install the required libraries using:
```bash
pip install requests pandas openpyxl
```
### Usage:
```bash
python Scraping_CMA_Typhoon_Data.py
```
### Input the year
```bash
Please enter the year: 2024
```
### Sample Output:
```bash
Year 2024 has the following typhoons:
TCNone (nameless, 热带低压)
TC2404 (PRAPIROON, 派比安)
TC2403 (GAEMI, 格美)
TC2402 (MALIKSI, 马力斯)
TC2401 (EWINIAR, 艾云尼)
```
### Input the TC number
```bash
Please enter the typhoon TC number (last four digits after TC): 2401
```

## Detailed data for the selected typhoon will be displayed, including attributes such as dateUTC, vmax, grade, lat, lon, and mslp.
```   tc_num name_cn  name_en       dateUTC       dateCST  vmax                  grade   lat    lon  mslp      attr
0    2401     艾云尼  EWINIAR  202405240600  202405241400    12    Tropical Depression   9.0  127.1  1003  analysis
1    2401     艾云尼  EWINIAR  202405240900  202405241700    12    Tropical Depression   9.1  127.1  1003  analysis
...
46   2401     艾云尼  EWINIAR  202405301200  202405302000    20         Tropical Storm  29.8  136.7   990  forecast
```
### Output data
```bash
Data for typhoon 2401 will be saved to the files `2024_TC2401.csv` and `2024_TC2401.xlsx`.
```



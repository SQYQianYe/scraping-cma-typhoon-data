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
### Sample Output:
```Please enter the year: 2024
Year 2024 has the following typhoons:
TCNone (nameless, 热带低压)
TC2404 (PRAPIROON, 派比安)
TC2403 (GAEMI, 格美)
TC2402 (MALIKSI, 马力斯)
TC2401 (EWINIAR, 艾云尼)
Please enter the typhoon TC number (last four digits after TC): 2401
typhoon_jsons_list_2024({"typhoonList":[[2929137,"nameless","热带低压",null,null,20240003,null,"stop"],[2929257,"PRAPIROON","派比安",2404,"2404",20240004,"雨神","start"],[2929285,"GAEMI","格美",2403,"2403",20240005,"一种非常细小、高度群居生活的昆虫；蚂蚁","start"],[2927830,"MALIKSI","马力斯",2402,"2402",20240002,"菲律宾语，快速的意思","stop"],[2924577,"EWINIAR","艾云尼",2401,"2401",20240001,"密克罗尼西亚楚克岛（Chuuk）传统的风暴之神","stop"]]})
```
## Detailed data for the selected typhoon will be displayed, including attributes such as dateUTC, vmax, grade, lat, lon, and mslp.
```   tc_num name_cn  name_en       dateUTC       dateCST  vmax                  grade   lat    lon  mslp      attr
0    2401     艾云尼  EWINIAR  202405240600  202405241400    12    Tropical Depression   9.0  127.1  1003  analysis
1    2401     艾云尼  EWINIAR  202405240900  202405241700    12    Tropical Depression   9.1  127.1  1003  analysis
...
46   2401     艾云尼  EWINIAR  202405301200  202405302000    20         Tropical Storm  29.8  136.7   990  forecast

```

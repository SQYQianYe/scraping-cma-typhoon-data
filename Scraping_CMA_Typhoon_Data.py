import requests
import json
import re
import time
import pandas as pd
import datetime

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def show_tc_nums_and_names_by_year(year):
    url = f"http://typhoon.nmc.cn/weatherservice/typhoon/jsons/list_{year}?callback=typhoon_jsons_list_{year}"
    html_obj = requests.get(url, headers=headers).text
    
    # Process the string to extract the useful JSON part
    json_obj = html_obj[html_obj.index("(") + 1:html_obj.rindex(")")]
    json_dict = json.loads(json_obj)
    
    # Parse the JSON data for typhoon numbers and names
    typhoon_list = json_dict.get("typhoonList", [])
    if typhoon_list:
        print(f"Year {year} has the following typhoons:")
        for typhoon in typhoon_list:
            num = f"TC{typhoon[3]}"
            name_cn = typhoon[2] if typhoon[2] != "null" else ""
            name_en = typhoon[1]
            print(f"{num} ({name_en}, {name_cn})")
    else:
        print(f"No typhoon information found for year {year}")

def date_pred(date, deltahour):
    """
    date: yyyymmddHHMM, string
    deltahour: hours, integer
    """
    time = datetime.datetime.strptime(date, "%Y%m%d%H%M")
    new_date = (time + datetime.timedelta(hours=deltahour)).strftime("%Y%m%d%H%M")
    return new_date

def get_type(date_type):
    item = {'TC': 'Tropical Cyclone', 'TD': 'Tropical Depression', 'TS': 'Tropical Storm', 'STS': 'Severe Tropical Storm',
            'TY': 'Typhoon', 'STY': 'Severe Typhoon', 'SuperTY': 'Super Typhoon', '': '',}
    return item.get(date_type, '')

def get_tc_info(item):
    t = int(round(time.time() * 1000)) # 13-digit timestamp
    # callback: typhoon_jsons_view_ + typhoon id
    url = 'http://typhoon.nmc.cn/weatherservice/typhoon/jsons/view_%s?t=%s&callback=typhoon_jsons_view_%s' % (item['id'], t, item['id'])
    html_obj = requests.get(url, headers=headers, verify=False).text
    data = json.loads(re.match(".*?({.*}).*", html_obj, re.S).group(1))['typhoon']

    # Create dictionary
    info_dicts = { 'tc_num':item['tc_num'],  # Number
                   'name_cn':item['name_cn'], # Chinese name
                   'name_en':item['name_en'], # English name
                   'dateUTC':[],    # Date UTC
                   'dateCST':[],    # Date CST
                   'vmax':[],    # Maximum wind speed m/s
                   'grade':[],   # Grade
                   'lat':[],   # Latitude deg
                   'lon':[],   # Longitude deg
                   'mslp':[],    # Central pressure hPa
                   'attr':[]}   # Attribute: forecast or analysis

    # Iterate through analysis data
    for v in data[8]:
        info_dicts['dateUTC'].append(v[1])
        info_dicts['dateCST'].append(date_pred(v[1], 8)) # UTC to CST
        info_dicts['vmax'].append(v[7])
        info_dicts['grade'].append(get_type(v[3]))
        info_dicts['lon'].append(v[4])
        info_dicts['lat'].append(v[5])
        info_dicts['mslp'].append(v[6])
        info_dicts['attr'].append('analysis')

    # Latest forecast time
    dateUTC0 = info_dicts['dateUTC'][-1]

    # Latest forecast
    if len(data[8][-1]) > 11 and data[8][-1][11] is not None and 'BABJ' in data[8][-1][11]:
        BABJ_list = data[8][-1][11]['BABJ']
        for i in range(len(BABJ_list)):
            pred_hour = int(BABJ_list[i][0]) # Forecast lead time in hours
            dateUTC_pred = date_pred(dateUTC0, pred_hour)
            info_dicts['dateUTC'].append(dateUTC_pred)
            info_dicts['dateCST'].append(date_pred(dateUTC_pred, 8))
            info_dicts['vmax'].append(BABJ_list[i][5])
            info_dicts['grade'].append(get_type(BABJ_list[i][7]))
            info_dicts['lon'].append(BABJ_list[i][2])
            info_dicts['lat'].append(BABJ_list[i][3])
            info_dicts['mslp'].append(BABJ_list[i][4])
            info_dicts['attr'].append('forecast')

    tc_info = pd.DataFrame(info_dicts)
    return tc_info

def get_tc_info_by_year_and_num(year, num):
    url = f"http://typhoon.nmc.cn/weatherservice/typhoon/jsons/list_{year}?callback=typhoon_jsons_list_{year}"
    
    html_obj = requests.get(url, headers=headers, verify=False).text
    print(html_obj)
    data = json.loads(re.match(".*?({.*}).*", html_obj, re.S).group(1))

    if data.get('typhoonList'):
        for item in data['typhoonList']:
            if item[4] == num:
                tc = {
                    'id': item[0],
                    'tc_num': str(item[4]),
                    'name_cn': item[2],
                    'name_en': item[1]
                }
                return get_tc_info(tc)
    return None

if __name__ == "__main__":

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    year = input("Please enter the year: ")
    show_tc_nums_and_names_by_year(year)
    num = input("Please enter the typhoon TC number (last four digits after TC): ")

    data = get_tc_info_by_year_and_num(year, num)

    if data is not None:
        print(data)
        data.to_csv(rf'{year}_TC{num}.csv', index=False)
        print(f"Data for typhoon {num} has been saved to file {year}_TC{num}.csv")
        data.to_excel(rf'{year}_TY{num}.xlsx', index=False, engine='openpyxl')
        print(f"Data for typhoon {num} has been saved to file {year}_TC{num}.xlsx")
    else:
        print(f"No data found for typhoon {num} in year {year}.")

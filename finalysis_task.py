# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 12:06:10 2022

@author: kshah23
"""

import pandas as pd
import urllib3
import ephem
from math import degrees
from datetime import datetime, timedelta
## Collect the data

def corr_matrix_cal(date, output_mode):
    # Intraday data
    cols = ['timestamp','open','high','low', 'close','volume']
    intraday_data = pd.read_csv('AAPL_FirstRateDatacom1.txt')
    intraday_data.columns = cols
    
    # Calculating 5 working days before the mentioned date
    num_days_to_subtract = 1
    prev_date_day = datetime.strptime(date, '%Y-%m-%d')
    
    # If Initial day is weekend, initializing matrix as empty, else, adding the first day
    if(prev_date_day.strftime("%A")=="Sunday" or prev_date_day.strftime("%A")=="Saturday"):
        days = []
    else:
        days = [prev_date_day.strftime('%A')]

    # Skipping count if there are Sundays or Saturdays in the counting range    
    while(len(days)!=5):
        day = (datetime.strptime(date, '%Y-%m-%d')- timedelta(days=num_days_to_subtract)).strftime('%A')
        if(day=='Saturday' or day=='Sunday'):
            num_days_to_subtract += 1
            continue
        else:
            days.append(day)
            num_days_to_subtract += 1
        
    # Replacing year to 2019 for matching purposes with AAPL data, later year reverted to 2022
    prev_date = str(datetime.strptime(date, '%Y-%m-%d') - timedelta(days=num_days_to_subtract-1)).replace('2022','2019')
    date = date.replace('2022','2019')

    # Filtering data in the date range
    filter_data = intraday_data[intraday_data['timestamp']>prev_date]
    filter_data = filter_data[filter_data['timestamp']<date]
    
    # Getting the initial value of the ISS
    http = urllib3.PoolManager()
    req = http.request("GET","http://celestrak.org/NORAD/elements/stations.txt")
    data = req.data.decode('utf-8')
    tle = data.split("\n")[0:3]
    line1 = tle[0]
    line2 = tle[1]
    line3 = tle[2]
    
    # Calculating space of the ISS based on AAPL timestamp
    times = filter_data['timestamp']
    iss_aapl_location_data = []
    # Reading the Initial position here
    iss = ephem.readtle(line1, line2, line3)
    ite = 0
    for t in times:
        # Reverting back to 2022
        to_find_time = t.replace('2019','2022')
        iss.compute(to_find_time)
        # Appending rows to final dataframe. Merging stock data and position data on 'timestamp' attribute.
        iss_aapl_location_data.append([to_find_time, degrees(iss.sublong), degrees(iss.sublat), filter_data.iloc[ite][1],
                                  filter_data.iloc[ite][2], filter_data.iloc[ite][3], filter_data.iloc[ite][4], filter_data.iloc[ite][5]])
        ite += 1
    iss_aapl_location_data = pd.DataFrame(iss_aapl_location_data)
    iss_aapl_location_data.columns = ['timestamp', 'longitude', 'latitude', 'open','high','low','close','volume']
    
    # Calculating the Correlation Matrix
    correlation_result = (iss_aapl_location_data.corr())
    
    # Writing the results to html and csv
    if(output_mode=='html'):
        correlation_result.to_html('iss_aapl_correlation_matrix.html')
    else:
        correlation_result.to_csv('iss_aapl_correlation_matrix.csv')
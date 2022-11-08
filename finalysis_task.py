# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 12:06:10 2022

@author: kshah23
"""

import pandas as pd
import time
import urllib3
import json
import datetime

import datetime
import ephem
from math import degrees
## Collect the data

# Intraday data
cols = ['timestamp','open','high','low', 'close','volume']
intraday_data = pd.read_csv('AAPL_FirstRateDatacom1.txt')
intraday_data.columns = cols

filter_data = intraday_data[intraday_data['timestamp']>'2019-11-03']
filter_data = filter_data[filter_data['timestamp']<'2019-11-08']


http = urllib3.PoolManager()
req = http.request("GET","http://celestrak.org/NORAD/elements/stations.txt")
data = req.data.decode('utf-8')
tle = data.split("\n")[0:3]
line1 = tle[0]
line2 = tle[1]
line3 = tle[2]

times = filter_data['timestamp']
iss_aapl_location_data = []
ite = 0
for t in times:
    iss = ephem.readtle(line1, line2, line3)
    to_find_time = t.replace('2019','2022')
    iss.compute(to_find_time)
    iss_aapl_location_data.append([to_find_time, degrees(iss.sublong), degrees(iss.sublat), filter_data.iloc[ite][1],
                              filter_data.iloc[ite][2], filter_data.iloc[ite][3], filter_data.iloc[ite][4], filter_data.iloc[ite][5]])
    ite += 1
iss_aapl_location_data = pd.DataFrame(iss_aapl_location_data)
iss_aapl_location_data.columns = ['timestamp', 'longitude', 'latitude', 'open','high','low','close','volume']

print(iss_aapl_location_data.corr())

#print(filter_data)
#iss_aapl_data = pd.merge(filter_data, iss_location_data, on="timestamp")
#print(iss_aapl_data)
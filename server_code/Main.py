# --------------------------------------------------
#   Market Capitalization Dashboard
# --------------------------------------------------
#   Author   : Tom Eleff
#   Version  : 1_1
#   Date     : 29MAY21
# --------------------------------------------------

import sys
import os
import datetime
import warnings
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd

# import xlrd
# import glob
# import itertools
# import pandas.io.formats.excel

# from openpyxl import load_workbook
# from openpyxl.styles import Font, Alignment, PatternFill
# from openpyxl.styles import NamedStyle
# from openpyxl.utils.dataframe import dataframe_to_rows
# from datetime import timedelta

# --------------------------------------------------
# Create Local Path Dictionary
# --------------------------------------------------

urlDict = {'valURL': 'https://www.federalreserve.gov/paymentsystems'
                     + '/files/coin_currcircvalue.txt',
           'volURL': 'https://www.federalreserve.gov/paymentsystems'
                     + '/files/coin_currcircvolume.txt',
           'exchURL': 'https://www.federalreserve.gov/datadownload/'
                      + 'Output.aspx?rel=H10'
                      + '&series=c5d6e0edf324b2fb28d73bcacafaaa02'
                      + '&lastobs=&from=01/01/2000&to=12/31/2021'
                      + '&filetype=csv&label=include&layout=seriescolumn'}

databaseLoc = os.path.dirname(__file__)
configDict = {'logPath': databaseLoc,
              'configPath': databaseLoc,
              'modulePath': databaseLoc + '/1. Modules',
              'outPath': databaseLoc + '/2. Database'}

# --------------------------------------------------
# Import Local Function Modules
# --------------------------------------------------

if databaseLoc not in sys.path:
    sys.path.append(os.path.abspath(databaseLoc))
    # print('Assigned Database Location: [' + databaseLoc + ']')

if configDict['modulePath'] not in sys.path:
    sys.path.append(os.path.abspath(configDict['modulePath']))
    # print('Assigned Module Location  : [' + configDict['modulePath'] + ']')

# import UtilModule as Util
import Request_Fed as ReqRed
import Request_Ticker as ReqYF

# --------------------------------------------------
# Assign Global Variables
# --------------------------------------------------

# Estimate Current Year Market Capitalization Value USD
estValue = True

# Forecast Period, Current Year + N Years
forecastPeriod = 0

# Requested Coin Ticker
ticker = 'ERG'

# Target Currency
fiat = 'USD'

date = str(datetime.datetime.now()).split(' ')[0]
year = datetime.datetime.now().year
startDate = str(year-21)+'-1-1'
endDate = date[:]
prevSource = ''
version = '1_1'

# --------------------------------------------------
# Create Log
# --------------------------------------------------

# Util.create_log(configDict, version, date)

# --------------------------------------------------
# Import Config
# --------------------------------------------------

# if 'conf.txt' in os.listdir(configDict['logPath']):
#     paramDict = Util.read_config(configDict)
#     Util.write_log(configDict,
#                    '\nNOTE: conf.txt Imported Successfully.')
# else:
#     Util.write_config(configDict, paramDict)
#     Util.write_log(configDict,
#                    '\nNOTE: conf.txt Created Successfully.')

# --------------------------------------------------
# Request
# --------------------------------------------------

# Federal Reserve
dfVal = ReqRed.request_circulation(configDict,
                                   urlDict['valURL'],
                                   'Value')
dfVol = ReqRed.request_circulation(configDict,
                                   urlDict['volURL'],
                                   'Volume')
dfExch = ReqRed.request_exchange(configDict,
                                 urlDict['exchURL'],
                                 'Exchange')

# Yahoo Finance (CoinMarketCap)
coinDict = ReqYF.request_mktdata(configDict, startDate,
                                 endDate, ticker+'-USD')

# --------------------------------------------------
# Produce Poly Fit
# --------------------------------------------------

# Generate 20 Year Period
yearLst = np.arange(year-21,
                    year+forecastPeriod,
                    1)

volLst = dfVol['Total'].to_numpy()
valLst = dfVal['Total'].to_numpy()

# Add to Arrays
for addYear in np.arange(year,
                         year+forecastPeriod,
                         1):
    volLst = np.append(volLst, np.nan)
    valLst = np.append(valLst, np.nan)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', np.RankWarning)
    valCoeffs = np.poly1d(np.polyfit(dfVol['Year'].to_numpy(),
                                     dfVal['Total'].to_numpy(),
                                     2))
    volCoeffs = np.poly1d(np.polyfit(dfVol['Year'].to_numpy(),
                                     dfVol['Total'].to_numpy(),
                                     2))

# --------------------------------------------------
# Produce Scenario Values
# --------------------------------------------------

# Estimate Market Capitalization Value USD
if estValue:
    latestValue = np.polyval(valCoeffs, year)
else:
    latestValue = valLst[-1]

multFactor = (latestValue * 1000000000) / coinDict['tickerVal']
estCoinPrice = round(coinDict['tickerPrice'] * multFactor)
coinGrowth = round((estCoinPrice / coinDict['tickerPrice'] - 1) * 100, 2)

print('Latest Value    : $'
      + str(round(latestValue, 2)) + 'B')
print('Ticker Value    : $'
      + str(round(coinDict['tickerVal']
            / 1000000000, 2))
      + 'B')
print('Ticker Price    : $'
      + str(round(coinDict['tickerPrice'], 2)))
print('Multiplier      : '
      + str(round(multFactor, 2)))
print('Est. Coin Price : $'
      + str(round(estCoinPrice, 2)))
print('% Growth        : '
      + str(round(coinGrowth, 2)) + '%')

# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, ax = plt.subplots()
ax.plot(yearLst,
        valLst,
        '.',
        color='red',
        alpha=1)
ax.plot(np.linspace(year-21, year+forecastPeriod, 100),
        valCoeffs(np.linspace(year-21, year+forecastPeriod, 100)),
        '-',
        color='red',
        alpha=0.3)
ax.set_xlabel('Year')
ax.set_ylabel('Value [$B]')

# ax2 = ax.twinx()
# ax2.plot(yearLst,
#          volLst,
#          '.',
#          color='blue',
#          alpha=0.5)
# ax2.plot(np.linspace(year-21, year+forecastPeriod, 100),
#          volCoeffs(np.linspace(year-21, year+forecastPeriod, 100)),
#          '-',
#          color='blue',
#          alpha=0.3)
# ax2.set_ylabel('Volume [Billions]')

plt.show()

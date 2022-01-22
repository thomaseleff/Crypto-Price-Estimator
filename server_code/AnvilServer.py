# --------------------------------------------------
#   Anvil Uplink Server
# --------------------------------------------------
#   Author   : Tom Eleff
#   Version  : 1_1
#   Date     : 30JUN21
# --------------------------------------------------

import schedule
import time
import os
import sys
import datetime
import warnings
import hashlib
import re
import numpy as np
import requests
import pandas as pd
import yfinance as yf
import anvil.server
import anvil.media
from anvil.tables import app_tables

# --------------------------------------------------
# Create Local Path Dictionary
# --------------------------------------------------

databaseLoc = os.path.dirname(__file__)
configDict = {'logPath': databaseLoc,
              'configPath': databaseLoc,
              'modulePath': databaseLoc + '/1. Modules',
              'outPath': databaseLoc + '/2. Database'}

# --------------------------------------------------
# Create Dictionaries
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

# --------------------------------------------------
# Assign Global Variables
# --------------------------------------------------

date = str(datetime.datetime.now()).split(' ')[0]
version = '1_1'
upLinkID = '4PEASWHJPSO4VUYS2M6FHD4X-V6YDNU752H23XGPB'

# --------------------------------------------------
# Connect to Client
# --------------------------------------------------

anvil.server.connect(upLinkID, quiet=True)

# --------------------------------------------------
# Import Local Function Modules
# --------------------------------------------------

if databaseLoc not in sys.path:
    sys.path.append(os.path.abspath(databaseLoc))
    # print('Assigned Database Location: [' + databaseLoc + ']')

if configDict['modulePath'] not in sys.path:
    sys.path.append(os.path.abspath(configDict['modulePath']))
    # print('Assigned Module Location  : [' + configDict['modulePath'] + ']')

import UtilModule as Util

# --------------------------------------------------
# Create Log
# --------------------------------------------------

Util.create_log(configDict, version, date)

# --------------------------------------------------
# Initialize Log Header
# --------------------------------------------------

# Output to Log
Util.output_header(configDict,
                   'Initialize Anvil App Connection',
                   'https://crypto-price-estimator.anvil.app')
Util.write_log(configDict,
               '\n')
Util.write_log(configDict,
               'NOTE: Uplink Established Successfully ['
               + upLinkID + '].')
Util.output_header(configDict,
                   'Anvil Client Requests',
                   'https://crypto-price-estimator.anvil.app')
Util.write_log(configDict,
               '\n')
Util.write_log(configDict,
               'MESSAGE		   '
               + 'SESSION HASH			               '
               + 'DATETIME                    '
               + 'ID    COIN     TARGET CURRENCY\n')
Util.write_log(configDict,
               '-----------------  '
               + '------------------------------------------  '
               + '--------------------------  ----  -------  '
               + '----------------------\n')

# --------------------------------------------------
# Define Request Functions
# --------------------------------------------------


def request_circulation(reqURL, metric):
    # reqURL               : URL to ASCII Datafile
    # metric               : Fed Reserve Metric Name

    # Request ASCII Datafile
    req = requests.get(reqURL)
    reqFile = req.text
    reqFile = reqFile.replace('$', ' ')
    reqFile = reqFile.replace(' to  ', '')

    # Output ASCII Datafile
    with open(configDict['outPath']
              + '/Fed Reserve ' + metric + '.txt', 'w') as file:
        file.write(reqFile)

    # Convert ASCII Datafile
    df = pd.read_csv(configDict['outPath'] + '/Fed Reserve ' + metric + '.txt',
                     engine='python',
                     sep=r'\s+',
                     skiprows=1,
                     header=0,
                     thousands=',',
                     names=['1', '2',
                            '5', '10', '20',
                            '50', '100',
                            '500to10K', 'Total'],
                     skipfooter=2)

    # Reset Index
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'Year'})

    # Convert to Numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    # Sort Columns
    df = df.sort_values(by=['Year'], ascending=True)

    # Overwrite ASCII Datafile
    df.to_csv(configDict['outPath'] + '/Fed Reserve ' + metric + '.txt',
              sep=',',
              index=False)

    # Populate DataTables
    if metric == 'Value':
        for d in df.to_dict(orient="records"):
            app_tables.value.add_row(**d)
    if metric == 'Volume':
        for d in df.to_dict(orient="records"):
            app_tables.volume.add_row(**d)


def request_exchange(reqURL, metric):
    # reqURL               : URL to ASCII Datafile
    # metric               : Fed Reserve Metric Name

    # Convert ASCII Datafile
    df = pd.read_csv(reqURL,
                     engine='python',
                     sep=',',
                     skiprows=(1, 2, 3, 4, 5),
                     header=0,
                     thousands=',',
                     names=['YearMonth',
                            'US-AUSTRALIA_DOLLAR',
                            'US-EMUCOUNTRIES_EURO',
                            'US-NEWZEALAND_DOLLAR',
                            'US-UNITEDKINGDOM_POUND',
                            'BRAZIL_REAL-US',
                            'CANADA_DOLLAR-US',
                            'CHINA_YUAN-US',
                            'DENMARK_KRONE-US',
                            'HONGKONG_DOLLAR-US',
                            'INDIA_RUPEE-US',
                            'JAPAN_YEN-US',
                            'MALAYSIA_RINGGIT-US',
                            'MEXICO_PESO-US',
                            'NORWAY_KRONE-US',
                            'SOUTHAFRICA_RAND-US',
                            'SINGAPORE_DOLLAR-US',
                            'SOUTHKOREA_WON-US',
                            'SRILANKA_RUPEE-US',
                            'SWEDEN_KRONA-US',
                            'SWITZERLAND_FRANC-US',
                            'TAIWAN_DOLLAR-US',
                            'THAILAND_BAHT-US',
                            'VENEZUELA_BOLIVAR-US'])

    # Summarize Yearly
    df['Year'] = df['YearMonth'].str[:4]
    df = df.groupby(by='Year').agg('mean')

    # Recalculate Metrics
    recalcVarLst = ['US-AUSTRALIA_DOLLAR', 'US-EMUCOUNTRIES_EURO',
                    'US-NEWZEALAND_DOLLAR', 'US-UNITEDKINGDOM_POUND']

    for var in recalcVarLst:
        varName = (var.split('-')[1] + '-'
                   + var.split('-')[0])
        df[varName] = 1 / df[var]

    # Keep Columns
    df = df[[col for col in df if col.endswith('US')]]

    # Reset Index
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'Year'})

    # Convert to Numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    # Sort Columns
    df = df.sort_values(by=['Year'], ascending=True)

    # Overwrite ASCII Datafile
    df.to_csv(configDict['outPath'] + '/Fed Reserve ' + metric + '.txt',
              sep=',',
              index=False)

    # Populate DataTables
    for d in df.to_dict(orient="records"):
        app_tables.exchange.add_row(**d)


def update_fed_reserve():

    # Output to Log
    Util.output_header(configDict,
                       'Update Anvil Database Tables',
                       'https://crypto-price-estimator.anvil.app')
    Util.write_log(configDict,
                   '\n')

    # Delete All Rows In DataTables
    app_tables.value.delete_all_rows()
    app_tables.volume.delete_all_rows()
    app_tables.exchange.delete_all_rows()

    # Output to Log
    Util.write_log(configDict,
                   'NOTE: Anvil Database Tables Cleared '
                   + 'Successfully.\n')

    # Request Federal Reserve Value
    request_circulation(urlDict['valURL'],
                        'Value')

    # Output to Log
    Util.write_log(configDict,
                   'NOTE: [value] Anvil Database Table Updated '
                   + 'Successfully.\n')

    # Request Federal Reserve Volume
    request_circulation(urlDict['volURL'],
                        'Volume')

    # Output to Log
    Util.write_log(configDict,
                   'NOTE: [volume] Anvil Database Table Updated '
                   + 'Successfully.\n')

    # Request Federal Reserve Exchange Rates
    request_exchange(urlDict['exchURL'],
                     'Exchange')

    # Output to Log
    Util.write_log(configDict,
                   'NOTE: [exchange] Anvil Database Table Updated '
                   + 'Successfully.')
    Util.output_header(configDict,
                       'Anvil Client Requests',
                       'https://crypto-price-estimator.anvil.app')
    Util.write_log(configDict,
                   '\n')
    Util.write_log(configDict,
                   'MESSAGE		   '
                   + 'SESSION HASH			               '
                   + 'DATETIME                    '
                   + 'ID    COIN     TARGET CURRENCY\n')
    Util.write_log(configDict,
                   '-----------------  '
                   + '------------------------------------------  '
                   + '--------------------------  ----  -------  '
                   + '----------------------\n')


@anvil.server.callable
def request_session(sessCounter, strdatetime):
    # sessCounter          : Integer ID for Session
    # strdatetime          : Start Datetime of Session

    # Session Info
    sessInfo = str(sessCounter).zfill(4) + str(strdatetime)

    # Return Sha-1 Session Hash
    sessHash = hashlib.sha1(sessInfo.encode('utf-8')
                            ).hexdigest()

    # Output to Log
    Util.write_log(configDict,
                   'NEW SESSION     :  ['
                   + str(sessHash) + ']  '
                   + str(strdatetime) + '\n')

    # Create Session Dictionary
    sessDict = {'sessID': str(sessCounter).zfill(4),
                'sessStart': str(strdatetime),
                'sessHash': str(sessHash)}

    # Return Session Dictionary
    return sessDict


@anvil.server.callable
def request_mktdata(startDate, endDate,
                    year, ticker,
                    estValue, forecastPeriod,
                    exchRate, selectedCurrency,
                    reqCounter, sessHash,
                    strdatetime):
    # startDate            : Start Date
    # endDate              : End Date
    # year                 : Current Year
    # ticker               : Yahoo Finance Ticker
    # estValue             : Estimate Current Year Market
    #                           Cap Value USD
    # forecastPeriod       : Number of Years to Forecast
    # exchRate             : Exchange Rate from US Dollar
    #                           to target currency
    # selectedCurrency     : Target Currency
    # reqCounter           : Client Request Counter
    # sessHash             : Sha-1 Session Hash
    # strdatetime          : Start Datetime of Request

    # Escape Special Characters from Ticker Value
    ticker = re.sub('[^-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890]', '',
                    ticker.upper())

    # Output to Log
    Util.write_log(configDict,
                   'CLIENT REQUEST  :  ['
                   + str(sessHash) + ']  '
                   + str(strdatetime) + '  '
                   + str(reqCounter).zfill(4) + '  '
                   + str(ticker) + '  '
                   + str(selectedCurrency) + '\n')

    # Request Data
    df = yf.download(tickers=ticker,
                     start=startDate,
                     end=endDate,
                     interval='1mo')

    # Request Financials
    tickerObj = yf.Ticker(ticker)

    # Reset Index
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'Date'})

    # Output Datafile
    df.to_csv(configDict['outPath'] + '/' + str(ticker) + '.txt',
              sep=',',
              index=False)

    # Create Financial Dataframe
    try:
        tickerDict = {'tickerVal': tickerObj.info['marketCap'],
                      'tickerVol': tickerObj.info['circulatingSupply'],
                      'tickerPrice': tickerObj.info['regularMarketPrice']}

        # --------------------------------------------------
        # Import Federal Reserve Tables
        # --------------------------------------------------

        # Import
        dfVol = pd.read_csv(configDict['outPath'] + '/Fed Reserve Volume.txt',
                            sep=',')
        dfVal = pd.read_csv(configDict['outPath'] + '/Fed Reserve Value.txt',
                            sep=',')

        # --------------------------------------------------
        # Produce Poly Fit
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Produce Scenario Values
        # --------------------------------------------------

        # Estimate Market Capitalization Value USD
        if estValue:
            latestValue = np.polyval(valCoeffs, year)
        else:
            latestValue = valLst[-1]

        multFactor = (latestValue * 1000000000) / tickerDict['tickerVal']
        estCoinPrice = round(tickerDict['tickerPrice'] * multFactor)
        coinGrowth = round((estCoinPrice / tickerDict['tickerPrice'] - 1)
                           * 100, 2)

        # print('Latest Value    : $'
        #       + str(round(latestValue, 2)) + 'B')
        # print('Ticker Value    : $'
        #       + str(round(tickerDict['tickerVal']
        #             / 1000000000, 2))
        #       + 'B')
        # print('Ticker Price    : $'
        #       + str(round(tickerDict['tickerPrice'], 2)))
        # print('Multiplier      : '
        #       + str(round(multFactor)))
        # print('Est. Coin Price : $'
        #       + str(round(estCoinPrice, 2)))
        # print('% Growth        : '
        #       + str(round(coinGrowth, 2)) + '%')

        reqDict = {'marketCap': round(latestValue * exchRate, 1),
                   'cryptoCap': round(tickerDict['tickerVal']
                                      / 1000000000 * exchRate, 1),
                   'coinPrice': round(tickerDict['tickerPrice']
                                      * exchRate, 2),
                   'estCoinPrice': round(estCoinPrice * exchRate),
                   'priceMult': round(multFactor),
                   'perGrowth': round(coinGrowth, 2)}

        # Output to Log
        Util.write_log(configDict,
                       'COMPLETED       :  ['
                       + str(sessHash) + ']  '
                       + str(strdatetime) + '  '
                       + str(reqCounter).zfill(4) + '  '
                       + str(ticker) + '  '
                       + str(selectedCurrency) + '\n')

        return reqDict

    except KeyError:
        reqDict = {'ERROR': ('Request Failed. Unable to Retrieve'
                             + ' Financials for [' + str(ticker) + '].')}

        # Output to Log
        Util.write_log(configDict,
                       'FAILED          :  ['
                       + str(sessHash) + ']  '
                       + str(strdatetime) + '  '
                       + str(reqCounter).zfill(4) + '  '
                       + str(ticker) + '  '
                       + str(selectedCurrency) + '\n')

        return reqDict

# --------------------------------------------------
# Schedule Tasks
# --------------------------------------------------


# Schedule Federal Reserve Requests Weekly
schedule.every().saturday.at('09:00').do(update_fed_reserve)

# --------------------------------------------------
# Listen For Client Requests
# --------------------------------------------------

while True:

    # Checks Status of Scheduled Task
    schedule.run_pending()

    # Wait for Client Requests
    time.sleep(1)

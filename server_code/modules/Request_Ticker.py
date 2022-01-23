# --------------------------------------------------
#   Request Stock Ticker Info from Yahoo Finance
# --------------------------------------------------
#   Author   : Tom Eleff
#   Version  : 1_1
#   Date     : 30MAY21
# --------------------------------------------------

import yfinance as yf
# import UtilModule as Util

# --------------------------------------------------
# Define Request Functions
# --------------------------------------------------


def request_mktdata(configDict, startDate,
                    endDate, ticker):
    # configDict           : Directory Path Dictionary
    # startYear            : Start Year
    # endYear              : End Year
    # ticker               : Yahoo Finance Ticker

    # Create Ticker Object
    tickerObj = yf.Ticker(ticker)

    # Request Data
    df = yf.download(tickers=ticker,
                     start=startDate,
                     end=endDate,
                     interval='1mo')

    # Request Financials
    tickerDict = {'tickerVal': tickerObj.info['marketCap'],
                  'tickerVol': tickerObj.info['circulatingSupply'],
                  'tickerPrice': tickerObj.info['regularMarketPrice']}

    # # Reset Index
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'Date'})

    # Output Datafile
    df.to_csv(configDict['outPath'] + '/' + ticker + '.txt',
              sep=',',
              index=False)

    # # Return Dictionary
    return tickerDict

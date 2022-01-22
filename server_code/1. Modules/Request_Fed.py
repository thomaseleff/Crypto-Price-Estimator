# --------------------------------------------------
#   Request US Federal Reserve Metrics
# --------------------------------------------------
#   Author   : Tom Eleff
#   Version  : 1_1
#   Date     : 23MAY21
# --------------------------------------------------

import requests
import pandas as pd
# import UtilModule as Util

# --------------------------------------------------
# Define Request Functions
# --------------------------------------------------


def request_circulation(configDict, reqURL, metric):
    # configDict           : Directory Path Dictionary
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

    # Return Dataframe
    return df


def request_exchange(configDict, reqURL, metric):
    # configDict           : Directory Path Dictionary
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
        varName = (var.split('/')[1] + '/'
                   + var.split('/')[0])
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

    # Return Dataframe
    return df

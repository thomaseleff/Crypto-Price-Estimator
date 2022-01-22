# --------------------------------------------------
#   Cryptocurrency Price Estimator
# --------------------------------------------------
#   Author   : Tom Eleff
#   Version  : 1_1
#   Date     : 29MAY21
# --------------------------------------------------

from ._anvil_designer import EstimatorTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go
import datetime

# --------------------------------------------------
# Create Dictionaries
# --------------------------------------------------

currencyICODict = {'UNITEDSTATES_DOLLAR':'USD',
                   'AUSTRALIA_DOLLAR':'AUD',
                   'BRAZIL_REAL':'BRL',
                   'CANADA_DOLLAR':'CAD',
                   'CHINA_YUAN':'CNY',
                   'DENMARK_KRONE':'DKK',
                   'EMUCOUNTRIES_EURO':'EUR',
                   'HONGKONG_DOLLAR':'HKD',
                   'INDIA_RUPEE':'INR',
                   'JAPAN_YEN':'JPY',
                   'MALAYSIA_RINGGIT':'MYR',
                   'MEXICO_PESO':'MXN',
                   'NEWZEALAND_DOLLAR':'NZD',
                   'NORWAY_KRONE':'NOK',
                   'SINGAPORE_DOLLAR':'SGD',
                   'SOUTHAFRICA_RAND':'ZAR',
                   'SOUTHKOREA_WON':'KRW',
                   'SRILANKA_RUPEE':'LKR',
                   'SWEDEN_KRONA':'SEK',
                   'SWITZERLAND_FRANC':'CHF',
                   'TAIWAN_DOLLAR':'TWD',
                   'THAILAND_BAHT':'THB',
                   'UNITEDKINGDOM_POUND':'GBP',
                   'VENEZUELA_BOLIVAR':'VES'}

# --------------------------------------------------
# Assign Global Variables
# --------------------------------------------------

# Estimate Current Year Market Capitalization Value USD
estValue = True

# Forecast Period, Current Year + N Years
forecastPeriod = 0

# Requested Coin Ticker
ticker = 'BTC'

# Target Currency
targetCurrency = 'United States [Dollar]'

# Session Counter
sessCounter = 0

# Request Counter
reqCounter = 0

# Date Time
date = str(datetime.datetime.now()).split(' ')[0]
year = datetime.datetime.now().year
startDate = str(year-21)+'-1-1'
endDate = date[:]


class Estimator(EstimatorTemplate):
  
  
  def __init__(self, **properties):
    global sessCounter, sessDict
    
    # Set Form Properties and Data Bindings.
    self.init_components(**properties)
    
    # Configure Session
    sessCounter += 1

    # Congfigure Initial Text Formats
    self.label_14.foreground = '#000000'
    self.label_14.bold = False

    # Congfigure Initial Text Values
    self.text_box_1.text = ticker
    self.drop_down_1.selected_value = targetCurrency
    self.label_7.text = '--'
    self.label_9.text = '--'
    self.label_11.text = '--'
    self.label_16.text = '--'
    self.label_12.text = '--'
    self.label_14.text = '--'

    # Request Session
    try:
      sessDict = anvil.server.call('request_session',
                                  sessCounter,
                                  str(datetime.datetime.now()))
    except anvil.server.UplinkDisconnectedError:
      
      # Disable Calculation Button
      self.primary_color_1.enabled = False
      
      # Output Status
      self.label_25.foreground = '#F44336'
      self.label_25.text = ('ERROR: Uplink Server is Not Connected.\n'
                            'Please Try Again Later.')

      
  def primary_color_1_click(self, **event_args):
    global reqCounter

    # Iterate Request Counter
    reqCounter += 1

    # Output Status
    self.label_25.foreground = '#2196F3'
    self.label_25.text = ('NOTE: Request Pending... Awaiting Results.\n'
                          + 'Refresh Page to Cancel.')
    
    # Reset Text Formats
    self.label_14.foreground = '#000000'
    self.label_14.bold = False

    # Reset Text Values
    self.label_6.text = ('Target Market Cap\n[Billions]')
    self.label_8.text = ('Crypto Market Cap\n[Billions]')
    self.label_10.text = ('Coin Price\n\n')
    self.label_15.text = ('Estimated Coin\nPrice')
    self.label_7.text = '--'
    self.label_9.text = '--'
    self.label_11.text = '--'
    self.label_16.text = '--'
    self.label_12.text = '--'
    self.label_14.text = '--'

    # Get Ticker Name, Accept Names like 'BTC' or 'BTC-USD'
    userTicker = self.text_box_1.text.replace(' ','')
    try:
      if userTicker.split('-')[1] == 'USD':
        reqTicker = userTicker
      else:
        reqTicker = userTicker.split('-')[0] + '-USD'
    except IndexError:
      reqTicker = userTicker + '-USD'

    # Get Exchange Rate
    selectedCurrency = self.drop_down_1.selected_value
    queryCurrency = self.drop_down_1.selected_value.replace(' [','_')
    queryCurrency = queryCurrency.replace(']','')
    queryCurrency = queryCurrency.replace(' ','')
    queryCurrency = queryCurrency.upper()

    if queryCurrency == 'UNITEDSTATES_DOLLAR':
      exchRate = 1
    else:
      exchRate = [row[queryCurrency+'-US'] for row in app_tables.exchange.search(Year=year)][0]
    
    # Request Cryptocurrency Metrics
    try:
      valDict = anvil.server.call('request_mktdata',
                                  startDate, endDate,
                                  year, reqTicker,
                                  estValue, forecastPeriod,
                                  exchRate, selectedCurrency,
                                  reqCounter, sessDict['sessHash'],
                                  str(datetime.datetime.now()))
      
      # Check if Request was Successful
      if 'ERROR' in valDict.keys():
        # Output Status
        self.label_25.foreground = '#F44336'
        self.label_25.text = 'ERROR: '+ valDict['ERROR']
  
      else:
        # Configure Label Values
        self.label_6.text = ('Target Market Cap\n[Billions '
                            + currencyICODict[queryCurrency] + ']')
        self.label_8.text = ('Crypto Market Cap\n[Billions '
                            + currencyICODict[queryCurrency] + ']')
        self.label_10.text = ('Coin Price\n['
                            + currencyICODict[queryCurrency] + ']')
        self.label_15.text = ('Estimated Coin\nPrice ['
                            + currencyICODict[queryCurrency] + ']')
        
        # Congfigure Text Formats
        if valDict['perGrowth'] > 100:
          self.label_14.foreground = '#4CAF50'
        elif valDict['perGrowth'] < 100:
          self.label_14.foreground = '#F44336'
        else:
          self.label_14.foreground = '#000000'
    
        self.label_14.bold = True
    
        # Congfigure Text Values
        self.label_7.text = '{:,.1f}'.format(valDict['marketCap'])
        self.label_9.text = '{:,.1f}'.format(valDict['cryptoCap'])
        self.label_11.text = '{:,.2f}'.format(valDict['coinPrice'])
        self.label_16.text = '{:,}'.format(valDict['estCoinPrice'])
        self.label_12.text = '{:,}'.format(valDict['priceMult'])
        self.label_14.text = '{:=+,.0f}'.format(valDict['perGrowth'])
        
        # Output Status
        self.label_25.foreground = '#4CAF50'
        self.label_25.text = 'NOTE: Request Complete.'

    except anvil.server.UplinkDisconnectedError:
    
      # Disable Calculation Button
      self.primary_color_1.enabled = False
      
      # Output Status
      self.label_25.foreground = '#F44336'
      self.label_25.text = ('ERROR: Uplink Server is Not Connected.\n'
                            'Please Try Again Later.')



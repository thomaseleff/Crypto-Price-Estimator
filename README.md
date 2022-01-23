# Cryptocurrency Price Estimator
The Cryptocurrency Price Estimator is a web application built through [anvil.works](https://anvil.works/) that generates a "what-if" scenario where if the market cap of a given cryptocurrency was to be equal to the current market cap of the United States [Dollar], what would be the resulting 'Coin Price' of the cryptocurrency in some 'Target Currency'.

![Web-App Animation](/assets/Calculate_Animation.gif)

# Features
- Supports all cryptocurrencies available from [Yahoo Finance](https://finance.yahoo.com/cryptocurrencies/) (currently over 350)
- Conversion of the United States - Dollar to 23 other currencies
- Weekly web-scraping of the US market cap (volume and value) and foreign exchange rates from [US Federal Reserve](https://www.federalreserve.gov)
- On demand web-scraping of the requested cryptocurrency 'Crypto Market Cap' and 'Coin Price' from [Yahoo Finance](https://finance.yahoo.com/cryptocurrencies/)

# Background
The Cryptocurrency Price Estimator is not to be interpreted as a forecast or a realistic expectation of the future 'Coin Price' of a requested cryptocurrency. **No result from this estimator constitutes financial advice**. The 'Coin Price' result of the estimator is derived from a hypothetical scenario where a single cryptocurrency is assumed to replace the entire United States money supply at the supply of the cryptocurrency today.

There are many determinations for the actual and future 'Crypto Market Cap' and 'Coin Price' of a given cryptocurrency. These factors are both uncontrolled (i.e. market behavior on cryptocurrency exchanges) and controlled (i.e. cryptocurrency white paper emission schedule), none of which this calculator considers.

'Target Market Cap' is always determined by the current market cap of the United States [Dollar]. If a different 'Target Currency' is provided other than the United States [Dollar], the US market cap is converted to the 'Target Currency' based on the foreign exchange rate between the United States [Dollar] and the 'Target Currency'. This conversion is also applied to the 'Crypto Market Cap', 'Coin Price' and 'Estimated Coin Price'. The US market cap and foreign exchange rates are web-scraped from the [US Federal Reserve](https://www.federalreserve.gov). The 'Crypto Market Cap' and 'Coin Price' are scraped from [Yahoo Finance](https://finance.yahoo.com/), which sources these metrics from [CoinMarketCap](https://coinmarketcap.com/).

# Usage
The Cryptocurrency Price Estimator is available at https://crypto-price-estimator.anvil.app/.

## Running a "What-If" Scenario
1. Navigate to https://crypto-price-estimator.anvil.app/ in a web-browser.
2. Open a second tab or window in the web-browser and navigate to https://finance.yahoo.com/cryptocurrencies/.
   - From the available cryptocurrencies at Yahoo Finance, select a cryptocurrency, making note of the [Symbol] (ticker) value for that cryptocurrency. These are often in the form of "BTC-USD" or "ALGO-USD".
3. Navigate back to the Cryptocurrency Price Estimator, and enter your desired 'Crypto Ticker' value from Yahoo Finance.

   - Values can be entered either like "BTC" or "BTC-USD"
4. From the 'Target Currency' drop-down, select the currency in which to display results.
5. Click 'CALCULATE' to generate results.
6. The message box should display '_NOTE: Request Complete._', indicating the request was successful.

In the rare case that the web-application is down, the message box will display '_ERROR: Uplink Server is Not Connected. Please Try Again Later._' in red text.
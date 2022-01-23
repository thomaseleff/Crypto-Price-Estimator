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
4. From the 'Target Currency' drop-down list, select the currency in which to display results.
5. Click 'CALCULATE' to generate results.
6. The message box should display '_NOTE: Request Complete._', indicating the request was successful.

In the rare case that the web-application is down, the message box will display '_ERROR: Uplink Server is Not Connected. Please Try Again Later._' in red text.

# Instructions
Anvil allows users to create and publish web applications with nothing but Python in an open-source environment. The easiest method for replicating this web application is to do so from a free account at [Anvil](https://anvil.works/).

## Cloning Cryptocurrency Price Estimator
The Crypocurrency Price Estimator requires both client and server code to execute. The client code can be cloned through [Anvil](https://anvil.works/) and the server code can be retrieved from the [/server_code](/server_code) folder of this repository.

### Cloning the Client Code
1. Navigate to [Anvil](https://anvil.works/) and create a new account or sign-in to an existing account.
2. Navigate to the following link, [Create a Clone of CryptoPriceEstimator_Dev](https://anvil.works/build#clone:ER7CIV2MZY7M2LOM=A6QP5KNZW76QG2PXW7U43AU6).
3. If required, continue to sign-in. Once signed-in, a pop-up window should appear titled "New Shared App". Within the pop-up window, click 'Make Copy'.

### Cloning the Server Code
The server code consists of all components in the [/server_code](/server_code) folder of this repository.

1. Navigate to the [Releases](https://github.com/thomaseleff/Crypto-Price-Estimator/releases) page and locate the most recent release.
2. Download either the ".zip" or ".tar.gz" file.
3. Verify the downloaded archive by evaluating the SHA-256 checksum of the archive against the corresponding checksum provided within the release notes. The checksums should match exactly, if they do not, do not unpack the archive. If the checksums match, proceed with preparing the server code.
4. Extract the archive to a local directory.

### Configuring Anvil Uplink
1. Navigate to [Anvil](https://anvil.works/) and then to the project page of your cloned app.
2. Configure an Uplink ID for the the newly cloned app.
   1. Click on the settings cog-wheel icon next to the name of the app in the upper left-hand corner of the screen. The name of the app should be "Clone of CryptoPriceEstimator_Dev".
   2. Within the drop-down list, select 'Uplink'.
   3. In the pop-up window, click the green button, 'Enable the Anvil Server Uplink for this app'.
   4. Make note of the provided uplink key.

### Installing Required Python Packages
1. From your python environment, run the following command, where {path to requirements.txt} is fully replaced (including the ellipses) with the file path to /server_code/requirements.txt in your local directory containing the extracted archive.

```
pip install -r {path to requirements.txt}
```

### Configuring server_config.json
server_config.json contains the uplink key for your cloned app so that the server code can successfully communicate with the client-side web application.

To modify server_config.json,

1. Open server_config.json in a text editor.
2. Replace the value for "upLinkID" with the uplink key for your cloned app (created in the **Configuring Anvil Uplink** section above).

### Editing Start_AnvilServer.bat (Optional)
Start_AnvilServer.bat executes the AnvilServer.py program. Alternatively, AnvilServer.py can be run by itself, without Start_AnvilServer.bat. 

1. Open Start_AnvilServer.bat in a text editor.
2. Replace the file path to python.exe with the corresponding file path for your installation of Python.
3. Replace the file path to AnvilServer.py with the file path to /server_code/AnvilServer.py in your local directory containing the extracted archive.

### Running Cryptocurrency Price Estimator
1. Navigate to the search box in the Windows Taskbar.
2. Search for "Command Prompt".
3. When results appear, open "Command Prompt".
4. When a new session window opens, run Start_AnvilServer.bat in the /server_code folder of the local directory containing the extracted archive.
   1. Alternatively, /server_code/AnvilServer.py can be run by itself instead.
5. Once running, you should see the Command Prompt window update with outputs from the server code.
6. Navigate to [Anvil](https://anvil.works/) and then to the project page for your cloned app.
7. At the top of the screen, click "Run".
8. Once the web application loads, click 'CALCULATE' to generate results.
9. If both the client and server code were cloned and configured correctly, the message box should display '_NOTE: Request Complete._', indicating the request was successful.
10. In the Command Prompt window, you should see a new session and new request logged within the output.

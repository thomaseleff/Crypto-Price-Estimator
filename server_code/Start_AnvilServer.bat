@ECHO OFF
:: This Batch File Starts the Anvil Uplink Server
TITLE Cryptocurrency Price Estimator Anvil Uplink

:: Start Up Anvil Uplink Server
ECHO Anvil Uplink Server is Running...
ECHO         Use Ctrl + C to Shutdown
ECHO.
"C:/Users/Tom Eleff/.edm/envs/Python3/python.exe" "T:\Documents\Projects\Anvil\CryptoPriceEstimator_Dev\server_code\AnvilServer.py" 2>&1

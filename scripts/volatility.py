# Import libraries for data analysis and visualization
import pandas as pd
import numpy as np
import yfinance as yf # Yahoo Finance data retrieval

# Daily Volatility

# Download daily historical data
ticker = 'AAPL'
data = yf.download(ticker, start='2023-01-01', end='2024-01-01', interval='1d')

# Calculate daily returns and daily volatility
data['Daily_Returns'] = data['Close'].pct_change()
data['Daily_Volatility'] = data['Daily_Returns'].rolling(window=21).std() * np.sqrt(252)  # Annualized daily volatility

# Display results
print(data[['Close', 'Daily_Volatility']].tail())

# Hourly Volatility

# Download hourly data
data_hourly = yf.download(ticker, start='2023-01-01', end='2024-01-01', interval='1h')

# Calculate hourly returns and volatility
data_hourly['Hourly_Returns'] = data_hourly['Close'].pct_change()
data_hourly['Hourly_Volatility'] = data_hourly['Hourly_Returns'].rolling(window=21).std() * np.sqrt(252*6.5)  # Assuming 6.5 hours in a trading day

# Display results
print(data_hourly[['Close', 'Hourly_Volatility']].tail())


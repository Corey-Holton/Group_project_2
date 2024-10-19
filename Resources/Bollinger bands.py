import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define Bollinger band Function
def calculate_bollinger_bands(historical_prices, window=20, std_dev=2):
    """Calculates Bollinger Bands for a given DataFrame."""
    historical_prices['SMA'] = historical_prices['Close'].rolling(window=window).mean()
    historical_prices['STD'] = historical_prices['Close'].rolling(window=window).std()
    historical_prices['Upper Band'] = historical_prices['SMA'] + (historical_prices['STD'] * std_dev)
    historical_prices['Lower Band'] = historical_prices['SMA'] - (historical_prices['STD'] * std_dev)
    return historical_prices

# Define Bollinger
def generate_signals(historical_prices):
    """Generates trading signals based on Bollinger Bands."""
    signals = []
    for i in range(len(historical_prices)):
        if historical_prices['Close'][i] > historical_prices['Upper Band'][i]:
            signals.append('Sell')
        elif historical_prices['Close'][i] < historical_prices['Lower Band'][i]:
            signals.append('Buy')
        else:
            signals.append('Hold')
    return signals

# Define dates
start_date = '2023-01-01'
end_date = '2024-01-01'

# Get S&P 500 tickers from Wikipedia
sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
# Filter out Class B shares that have a '.B' in the ticker name
sp500_tickers = [ticker for ticker in sp500_tickers if '.B' not in ticker]
print(f"Initial total S&P 500 tickers: {len(sp500_tickers)}")

# Download historical prices for the S&P 500 tickers
historical_prices = yf.download(sp500_tickers, start=start_date, end=end_date)

# Ensure we are working with Adjusted Close prices
historical_prices = historical_prices['Adj Close']
historical_prices = historical_prices.dropna(axis=1, how='all')  # Drop tickers with all NaN values
print(f"Successfully downloaded tickers: {len(historical_prices.columns)}")

# Transpose the dataframe for calculation
historical_prices = historical_prices.T

# Calculate Bollinger Bands for each ticker
historical_prices = historical_prices.apply(lambda x: calculate_bollinger_bands(x.to_frame(name='Close')), axis=1)

# Generate signals for each ticker
historical_prices['Signal'] = historical_prices.apply(lambda x: generate_signals(x), axis=1)

# Plot the data for a sample stock (e.g., 'AAPL')
ticker_sample = 'AAPL'
data_sample = historical_prices.loc[ticker_sample]

plt.figure(figsize=(14, 7))
plt.plot(data_sample.index, data_sample['Close'], label='Close')
plt.plot(data_sample.index, data_sample['SMA'], label='SMA')
plt.plot(data_sample.index, data_sample['Upper Band'], label='Upper Band')
plt.plot(data_sample.index, data_sample['Lower Band'], label='Lower Band')
plt.legend()
plt.title(f'{ticker_sample} Bollinger Bands')
plt.show()

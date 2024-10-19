# Import dependencies
import yfinance as yf
import pandas as pd
import numpy as np
from tqdm import tqdm

# Define dates
start_date = '2000-01-01'
end_date = '2024-10-14'

# Get S&P 500 tickers from Wikipedia
sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
# Filter out Class B shares that have a '.B' in the ticker name
sp500_tickers = [ticker for ticker in sp500_tickers if '.B' not in ticker]
print(f"Total S&P 500 tickers: {len(sp500_tickers)}")

# Download historical prices for the list of tickers
historical_prices = yf.download(sp500_tickers, start=start_date, end=end_date)['Adj Close']
# Fill NaN values with 0
historical_prices.fillna(0, inplace=True)
print(f"Successfully downloaded tickers: {len(historical_prices.columns)} out of {len(sp500_tickers)}")

# Function to calculate RSI
def calculate_rsi(historical_prices, window=14):
    # Ensure calculations are performed on the 'Adj Close' column
    delta = historical_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate RSI for all tickers
rsis = []
for ticker in tqdm(sp500_tickers):
    try:
        ticker_data = yf.download(ticker, start=start_date, end=end_date)
        ticker_data['RSI'] = calculate_rsi(ticker_data['Adj Close'])
        ticker_data['Ticker'] = ticker
        rsis.append(ticker_data)
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# Concatenate all the data into a single DataFrame
rsi_df = pd.concat(rsis)

# Select and rename relevant columns
rsi_df = rsi_df.reset_index()[['Date', 'Ticker', 'Adj Close', 'RSI']]
rsi_df.rename(columns={'Adj Close': 'Adjusted Close'}, inplace=True)

# Display the DataFrame
print(rsi_df.head())

# Save to CSV
rsi_df.to_csv('sp500_rsi_data.csv', index=False)

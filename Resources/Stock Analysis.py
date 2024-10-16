import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download stock data (replace 'AAPL' with your preferred ticker)
ticker = 'AAPL'
data = yf.download(ticker, start='2023-01-01', end='2024-01-01')

# Calculate Moving Averages
data['20_SMA'] = data['Close'].rolling(window=20).mean()
data['50_SMA'] = data['Close'].rolling(window=50).mean()

# Calculate RSI
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# Plot Close Price, Moving Averages, and RSI
plt.figure(figsize=(14, 8))

# Price and Moving Averages
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['20_SMA'], label='20-Day SMA', color='orange')
plt.plot(data['50_SMA'], label='50-Day SMA', color='green')
plt.title(f'{ticker} Stock Analysis')
plt.legend()

# RSI
plt.subplot(3, 1, 2)
plt.plot(data['RSI'], label='RSI', color='purple')
plt.axhline(70, color='red', linestyle='--')
plt.axhline(30, color='green', linestyle='--')
plt.title('Relative Strength Index')
plt.legend()

# Volume
plt.subplot(3, 1, 3)
plt.bar(data.index, data['Volume'], color='grey', label='Volume')
plt.title('Volume')
plt.legend()

plt.tight_layout()
plt.show()

#Triangle Patterns
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Download stock data
ticker = 'AAPL'
data = yf.download(ticker, start='2023-01-01', end='2024-01-01')
data['High_Peaks'], _ = find_peaks(data['High'])
data['Low_Troughs'], _ = find_peaks(-data['Low'])

# Visualize the peaks and troughs
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['High_Peaks'], data['High'][data['High_Peaks']], "x", label='High Peaks')
plt.plot(data['Low_Troughs'], data['Low'][data['Low_Troughs']], "o", label='Low Troughs')
plt.title(f'{ticker} Triangle Pattern Detection')
plt.legend()
plt.show()

# Head and Shoulders Patterns
# Assume peaks are stored in `data['High_Peaks']` and troughs in `data['Low_Troughs']`
# Define logic to identify head and shoulders based on peak heights and positions
# For simplicity, manual checking for illustration purposes:

# Support and Resistance Levels

# Identify potential support and resistance levels
data['Support_Level'] = data['Low'].rolling(window=20).min()
data['Resistance_Level'] = data['High'].rolling(window=20).max()

# Plot support and resistance
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Support_Level'], label='Support', linestyle='--', color='red')
plt.plot(data['Resistance_Level'], label='Resistance', linestyle='--', color='green')
plt.title(f'{ticker} Support and Resistance Levels')
plt.legend()
plt.show()

import pandas as pd
import numpy as np

def find_head_and_shoulders(df, price_column='Close'):
    """Finds head and shoulders patterns in a given price series."""

    # Find local maxima (potential heads)
    maxima = df.loc[df[price_column].shift(1) < df[price_column]]
    maxima = maxima.loc[df[price_column].shift(-1) < df[price_column]]

    # Find local minima (potential shoulders)
    minima = df.loc[df[price_column].shift(1) > df[price_column]]
    minima = minima.loc[df[price_column].shift(-1) > df[price_column]]

    patterns = []

    for i in range(1, len(maxima) - 1):
        left_shoulder = minima.loc[minima.index < maxima.index[i]]
        right_shoulder = minima.loc[minima.index > maxima.index[i]]

        if left_shoulder.empty or right_shoulder.empty:
            continue

        left_shoulder = left_shoulder.iloc[-1]
        right_shoulder = right_shoulder.iloc[0]

        head = maxima.iloc[i]

        # Check if the pattern meets the criteria
        if (
            head[price_column] > left_shoulder[price_column]
            and head[price_column] > right_shoulder[price_column]
            and abs(left_shoulder[price_column] - right_shoulder[price_column]) < 0.1 * head[price_column]  # Neckline should be relatively flat
        ):
            patterns.append({
                'left_shoulder': left_shoulder.name,
                'head': head.name,
                'right_shoulder': right_shoulder.name,
                'neckline': (left_shoulder[price_column] + right_shoulder[price_column]) / 2
            })

    return patterns

# Example usage
if __name__ == '__main__':
    # Load your price data
    df = pd.read_csv('your_data.csv')

    # Find head and shoulders patterns
    patterns = find_head_and_shoulders(df)

    for pattern in patterns:
        print(pattern)
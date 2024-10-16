# Bollinger bands

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_bollinger_bands(data, window=20, std_dev=2):
    """Calculates Bollinger Bands for a given DataFrame."""
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper Band'] = data['SMA'] + (data['STD'] * std_dev)
    data['Lower Band'] = data['SMA'] - (data['STD'] * std_dev)
    return data

def generate_signals(data):
    """Generates trading signals based on Bollinger Bands."""
    signals = []
    for i in range(len(data)):
        if data['Close'][i] > data['Upper Band'][i]:
            signals.append('Sell')
        elif data['Close'][i] < data['Lower Band'][i]:
            signals.append('Buy')
        else:
            signals.append('Hold')
    return signals

# Load your data (replace with your data source)
data = pd.read_csv('your_data.csv')

# Calculate Bollinger Bands
data = calculate_bollinger_bands(data)

# Generate signals
data['Signal'] = generate_signals(data)

# Plot the data
plt.plot(data['Close'], label='Close')
plt.plot(data['SMA'], label='SMA')
plt.plot(data['Upper Band'], label='Upper Band')
plt.plot(data['Lower Band'], label='Lower Band')
plt.legend()
plt.show()
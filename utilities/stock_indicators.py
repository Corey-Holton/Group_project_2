import numpy as np

# Define RSI function
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

# Define Bollinger Band function
def calculate_bollinger_bands(data, window=20):
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    return upper_band, lower_band

def calculate_daily_volatility(prices):
    returns = prices.pct_change(fill_method=None)
    volatility = returns.rolling(window=21).std() * np.sqrt(252)  # Annualized daily volatility
    return volatility
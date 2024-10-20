import numpy as np
import pandas as pd

def predict_signal(today_to_tomorrow, yesterday_to_today, prev_action):
    """
    Predict the trading signal based on the difference between today's and tomorrow's prices
    and yesterday's and today's prices.

    Parameters:
    today_to_tomorrow (float): The difference between today's and tomorrow's prices.
    yesterday_to_today (float): The difference between yesterday's and today's prices.
    prev_action (str): The previous trading action.

    Returns:
    str: The trading signal, which can be one of the following: [buy, hold, short, sell].
    """

    # If either `today_to_tomorrow` or `yesterday_to_today` difference is NaN, return NA
    if pd.isna(today_to_tomorrow) or pd.isna(yesterday_to_today):
        return pd.NA
    
    # Define a signal map to determine the action based on the difference values
    signal_map = {
        (1, -1): "buy",    # Buy signal: rising tomorrow, falling today
        (1, 1): "hold",    # Hold signal: rising tomorrow and today
        (0, 1): "hold",    # Hold signal: no change tomorrow, rising today
        (1, 0): "hold",    # Hold signal: rising tomorrow, no change today
        (-1, 1): "sell",   # Sell signal: falling tomorrow, rising today
        (-1, -1): "short", # Short signal: falling tomorrow and today
        (0, -1): "short",  # Short signal: no change tomorrow, falling today
        (-1, 0): "short",  # Short signal: falling tomorrow, no change today
    }

    # If the difference values are in the signal map...
    # Return the corresponding signal from the map: [buy, hold, short, sell]
    if (today_to_tomorrow, yesterday_to_today) in signal_map:
        return signal_map[(today_to_tomorrow, yesterday_to_today)]
    
    # If the difference values are both zero...
    # Handle neutral signals (when both today-to-tomorrow and yesterday-to-today) are zero
    if (today_to_tomorrow, yesterday_to_today) == (0, 0):
        # If there is a previous action...
        # return hold if the previous action was `buy` or `hold`, otherwise return `short`
        if not pd.isna(prev_action):
            return "hold" if prev_action in ["buy", "hold"] else "short"
        return pd.NA

    # Return NA for any other cases
    return pd.NA


def generate_trading_signals (df, ticker):
    """
    Generate trading signals based on the difference between today's and tomorrow's prices
    and yesterday's and today's prices.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the price data.
    ticker (str): The column name for which to generate the trading signals.

    Returns:
    pd.Series: The trading signals for the input DataFrame.
    """
    
    next_day = df[ticker].shift(-1)  # Next day's price data
    prev_day = df[ticker].shift(1)  # Previous day's price data

    # Calculate the difference between today's and tomorrow's prices and yesterday's and today's prices
    # (+1: rise, -1: fall, 0: no change)
    today_to_tomorrow = np.sign(next_day - df[ticker])
    yesterday_to_today = np.sign(df[ticker] - prev_day)

    # Initialize the action column with NA
    # This column will store the action signals for each day: [buy, hold, short, sell]
    actions = pd.Series(
        pd.NA,
        index=df.index
    )

    # Iterate over the rows and apply the predict_signal function
    for i in range(1, len(df)):
        prev_action = actions.iloc[i - 1] if i > 0 else pd.NA
        actions.iloc[i] = predict_signal(
            today_to_tomorrow.iloc[i], yesterday_to_today.iloc[i], prev_action)

    return actions
import numpy as np
import pandas as pd


def calculate_signals(today_to_tomorrow, yesterday_to_today):
    """
    Calculate the primary trading signals based on price differences.

    Parameters:
    today_to_tomorrow (pd.Series): The difference between today's and tomorrow's prices.
    yesterday_to_today (pd.Series): The difference between yesterday's and today's prices.

    Returns:
    pd.Series: The initial trading signals [excluding neutral cases (where both differences are zero)].
    """
    # Define conditions and their corresponding actions
    conditions = [
        (today_to_tomorrow == 1) & (yesterday_to_today == -1),  # Buy signal: rising tomorrow, falling today
        (today_to_tomorrow == 1) & (yesterday_to_today == 1),   # Hold signal: rising tomorrow and today
        (today_to_tomorrow == 0) & (yesterday_to_today == 1),   # Hold signal: no change tomorrow, rising today
        (today_to_tomorrow == 1) & (yesterday_to_today == 0),   # Hold signal: rising tomorrow, no change today
        (today_to_tomorrow == -1) & (yesterday_to_today == 1),  # Sell signal: falling tomorrow, rising today
        (today_to_tomorrow == -1) & (yesterday_to_today == -1), # Short signal: falling tomorrow and today
        (today_to_tomorrow == 0) & (yesterday_to_today == -1),  # Short signal: no change tomorrow, falling today
        (today_to_tomorrow == -1) & (yesterday_to_today == 0)   # Short signal: falling tomorrow, no change today
    ]

    choices = ["buy", "hold", "hold", "hold", "sell", "short", "short", "short"]

    # Vectorized signal assignment based on conditions
    # Vectorized means that the operation is applied to the entire Series at once rather than row by row
    initial_actions = pd.Series(
        np.select(
            conditions,     # Conditions to check
            choices,        # Actions to take if the condition is true
            default=pd.NA   # Default action if no condition is true (Not Available)
        ),
        index=today_to_tomorrow.index
    )

    # Return the initial signals (without handling neutral cases)
    return initial_actions


def handle_neutral_cases(actions, today_to_tomorrow, yesterday_to_today):
    """
    Handle neutral cases where both today-to-tomorrow and yesterday-to-today differences are zero.
    This function updates the action based on the previous action.

    Parameters:
    actions (pd.Series): The current set of actions.
    today_to_tomorrow (pd.Series): The difference between today's and tomorrow's prices.
    yesterday_to_today (pd.Series): The difference between yesterday's and today's prices.

    Returns:
    pd.Series: The updated actions with neutral cases handled.
    """
    # Mask for neutral cases (both differences are zero)
    # A mask is a boolean array that can be used to filter rows based on a condition
    # In this case, we want to filter rows where both differences are zero
    neutral_mask = (today_to_tomorrow == 0) & (yesterday_to_today == 0)

    # Shift the actions Series to get the previous action for each row
    # This is necessary to determine the action for the neutral cases
    prev_actions = actions.shift(1)

    # Update neutral cases based on previous action
    # Syntax: `np.where(condition, value_if_true, value_if_false)``
    
    actions.loc[neutral_mask] = np.where(

        # Condition (Outer `where`): Where previous action is buy or hold
        prev_actions.loc[neutral_mask].isin(["buy", "hold"]), 
        
        # Value if true: "hold"
        "hold", 

        # Value if false: Check if previous action is short or sell
        np.where( 
            # Condition (Inner `where`): Where previous action is short or sell
            prev_actions.loc[neutral_mask].isin(["short", "sell"]),

            # Value if true: "short"
            "short",

            # Value if false: Not Available (NA)
            pd.NA
        )
    )

    # Return the updated actions
    return actions


def generate_trading_signals(df, ticker):
    """
    Generate trading signals by first calculating primary signals and then handling neutral cases.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the price data.
    ticker (str): The column name for which to generate the trading signals.

    Returns:
    pd.Series: The trading signals for the input DataFrame.
    """

    # Shift the data to get the price differences
    next_day = df[ticker].shift(-1)  # Next day's price data
    prev_day = df[ticker].shift(1)   # Previous day's price data

    # Calculate the difference between today's and tomorrow's prices and yesterday's and today's prices
    today_to_tomorrow = np.sign(next_day - df[ticker])
    yesterday_to_today = np.sign(df[ticker] - prev_day)

    # Part 1: Calculate primary signals
    actions = calculate_signals(today_to_tomorrow, yesterday_to_today)

    # Part 2: Handle neutral cases based on previous action (Where both differences are zero)
    actions = handle_neutral_cases(actions, today_to_tomorrow, yesterday_to_today)

    return actions
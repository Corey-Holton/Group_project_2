import numpy as np

def generate_directions(data):
  next_day = data.shift(-1)  # Next day's price data
  prev_day = data.shift(1)   # Previous day's price data

  today_to_tomorrow = np.sign(next_day - data)
  yesterday_to_today = np.sign(data - prev_day)

  return today_to_tomorrow, yesterday_to_today
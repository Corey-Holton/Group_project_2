#Simple Moving Average (SMA)
# importing Libraries

# importing pandas as pd
import pandas as pd

# importing numpy as np
# for Mathematical calculations
import numpy as np

# importing pyplot from matplotlib as plt
# for plotting graphs
import matplotlib.pyplot as plt
plt.style.use('default')
%matplotlib inline

# importing time-series data
reliance = pd.read_csv('RELIANCE.NS.csv', index_col='Date',
					parse_dates=True)

# Printing dataFrame
reliance.head()

# Extract 'Close' column and convert to DataFrame
reliance = reliance['Close'].to_frame()

# Calculate 30-day Simple Moving Average (SMA)
reliance['SMA30'] = reliance['Close'].rolling(30).mean()

# Remove NULL values
reliance.dropna(inplace=True)

# Print DataFrame
reliance

# plotting Close price and simple
# moving average of 30 days using .plot() method
reliance[['Close', 'SMA30']].plot(label='RELIANCE', 
								figsize=(16, 8))

# Cumulative Moving Average (CMA)

# importing Libraries

# importing pandas as pd
import pandas as pd

# importing numpy as np
# for Mathematical calculations
import numpy as np

# importing pyplot from matplotlib as plt
# for plotting graphs
import matplotlib.pyplot as plt
plt.style.use('default')
%matplotlib inline

# importing time-series data
reliance = pd.read_csv('RELIANCE.NS.csv', 
					index_col='Date',
					parse_dates=True)

# Printing dataFrame
reliance.head()

# Extract and isolate 'Close' column, converting to DataFrame
reliance = reliance['Close'].to_frame()

# Calculate Cumulative Moving Average (CMA) with a window of 30
reliance['CMA30'] = reliance['Close'].expanding().mean()

# Print DataFrame
reliance

# plotting Close price and cumulative moving
# average of 30 days using .plot() method
reliance[['Close', 'CMA30']].plot(label='RELIANCE', 
								figsize=(16, 8))

Cumulative Moving Average (CMA)
# importing Libraries

# importing pandas as pd
import pandas as pd

# importing numpy as np
# for Mathematical calculations
import numpy as np

# importing pyplot from matplotlib as plt
# for plotting graphs
import matplotlib.pyplot as plt
plt.style.use('default')
%matplotlib inline

# importing time-series data
reliance = pd.read_csv('RELIANCE.NS.csv',
					index_col='Date',
					parse_dates=True)

# Printing dataFrame
reliance.head()

# Extract and isolate 'Close' column, converting to DataFrame
reliance = reliance['Close'].to_frame()

# Calculate Exponential Moving Average (EWMA) with a span of 30
reliance['EWMA30'] = reliance['Close'].ewm(span=30).mean()

# Print DataFrame
reliance

# plotting Close price and exponential 
# moving averages of 30 days
# using .plot() method
reliance[['Close', 'EWMA30']].plot(label='RELIANCE',
								figsize=(16, 8))

import pandas as pd
import yfinance as yf

from datetime import datetime
from utilities.print_utils import print_title, print_label, print_footer

# ================================================
# Utility to Print Report
# ================================================
def print_download_report_historical(data, sp500_tickers, start_date, end_date):
    """
    Print the download report for the S&P 500 data.

    Parameters:
    - data: DataFrame with historical prices for S&P 500 tickers
    - sp500_tickers: List of S&P 500 tickers
    - start_date: Start date for the data download
    - end_date: End date for the data download: if not provided, it will default to today's date
    """
    BORDER_COLOR = "blue"
    REQUEST_TEXT_COLOR = "bright_blue"
    RESPONSE_TEXT_COLOR = "bright_yellow"
    FOOTER_TEXT_COLOR = "bright_black"

    print_title("Download Report for S&P 500 `adj close`", REQUEST_TEXT_COLOR, BORDER_COLOR, closed_corners=False)

    # Check if data was successfully downloaded
    downloaded_tickers = data.columns.unique()
    successful_tickers_count = len(downloaded_tickers)
    total_tickers_count = len(sp500_tickers)

    # Get the actual date range of the downloaded data
    actual_start_date = data.index.min().strftime('%Y-%m-%d')
    actual_end_date = data.index.max().strftime('%Y-%m-%d')

    print_label("Total Requested Tickers:", str(total_tickers_count), REQUEST_TEXT_COLOR, BORDER_COLOR)
    print_label("Total Downloaded Tickers:", str(successful_tickers_count), RESPONSE_TEXT_COLOR, BORDER_COLOR)
    print_label("Requested Date Range:", f"{start_date} to {end_date}", REQUEST_TEXT_COLOR, BORDER_COLOR)
    print_label("Downloaded Date Range:", f"{actual_start_date} to {actual_end_date}", RESPONSE_TEXT_COLOR, BORDER_COLOR)
    print_footer("S&P 500 Data Downloaded Successfully...", FOOTER_TEXT_COLOR, BORDER_COLOR)

def print_download_report_today(data, sp500_tickers, time):
    """
    Print the download report for the S&P 500 data for today.

    Parameters:
    - data: DataFrame with historical prices for S&P 500 tickers
    - sp500_tickers: List of S&P 500 tickers
    - time: Time to fetch the data for
    """
    BORDER_COLOR = "blue"
    REQUEST_TEXT_COLOR = "bright_blue"
    RESPONSE_TEXT_COLOR = "bright_yellow"
    FOOTER_TEXT_COLOR = "bright_black"

    # Check if data was successfully downloaded
    total_tickers_count = len(sp500_tickers)

    # Get the actual date range of the downloaded data
    actual_date = data.index.max().strftime('%Y-%m-%d')

    print_title(f"Download Report for S&P 500  `close` for {actual_date}", REQUEST_TEXT_COLOR, BORDER_COLOR, closed_corners=False)

    print_label("Total Requested Tickers:", str(total_tickers_count), REQUEST_TEXT_COLOR, BORDER_COLOR)
    print_label("Requested Time:", time, REQUEST_TEXT_COLOR, BORDER_COLOR)
    print_label("Downloaded Date:", actual_date, RESPONSE_TEXT_COLOR, BORDER_COLOR)
    print_footer("S&P 500 Data Downloaded Successfully...", FOOTER_TEXT_COLOR, BORDER_COLOR)

# ================================================
# Fetching Historical Data
# ================================================
def fetch_and_download_sp500_data(start_date='2020-10-01', end_date=None):
    """
    Fetch and download historical adjusted close prices for S&P 500 tickers.

    Returns:
    - data: DataFrame with historical prices for S&P 500 tickers
    """
    # Set end date to today if not provided
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    # Fetch S&P 500 tickers

    #Get tickers from wikipedia
    sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].to_numpy()

    # Filter out Class B shares that have a '.B' in the ticker name
    # Class B shares are typically held by company insiders and have different voting rights than Class A shares
    sp500_tickers = [ticker for ticker in sp500_tickers if '.B' not in ticker]

    # Define dates for historical data download
    start_date = start_date
    end_date = end_date

    try:
        # Download historical prices
        data = yf.download(sp500_tickers, start=start_date, end=end_date)['Adj Close']

        # Fill NaN values with 0
        data.fillna(0, inplace=True)

        # Print download report
        print_download_report_historical(data, sp500_tickers, start_date, end_date)

    except Exception as e:
        # Handle any errors that occur during the download
        print_title(
            f"Failed to download data: {str(e)}", "bright_red", "red")
        
    return data

# ================================================
# Fetching Data for Today
# ================================================
def fetch_ticker_data(ticker_symbol, time):
    """ 
    Fetches the stock data for a given ticker symbol at 3:59 PM

    Parameters:
    - ticker_symbol: The stock ticker symbol to fetch data for.
    - time: The time to fetch the stock data for. Default is 3:59 PM.

    Returns:
    - data: The stock data for the given ticker symbol at 3:59 PM.
    """
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d", interval="1m")
    data["Ticker"] = ticker_symbol

    # Filter for 3:59 PM data
    three_fifty_nine_pm_mask = data.index.time == pd.Timestamp(time).time()
    data = data[three_fifty_nine_pm_mask]

    return data

def process_dataframe(dataframe):
    """ 
    Process the DataFrame to only include the Ticker and Close columns.

    Parameters:
    - dataframe: The DataFrame to process.

    Returns:
    - processed_dataframe: The processed DataFrame with only the Ticker and Close columns.
    """

    # Columns to drop from the DataFrame
    columns_to_drop = ['Open', 'High', 'Low', "Volume", "Dividends", "Stock Splits"]
    dataframe.drop(columns=columns_to_drop, inplace=True)

    dataframe.sort_values(by=["Datetime", "Ticker"], inplace=True)
    return dataframe[["Ticker", "Close"]]

def reshape_dataframe(dataframe):
    """
    Reshape the DataFrame to have the Ticker as columns and the Datetime as the index.

    Parameters:
    - dataframe: The DataFrame to reshape.

    Returns:
    - reshaped_dataframe: The reshaped DataFrame with the Ticker as columns and the Datetime as the index.
    """
    dataframe.reset_index(inplace=True)
    reshaped_dataframe = dataframe.pivot(index='Datetime', columns='Ticker', values='Close')
    return reshaped_dataframe

def sp500_data_for_today(time="15:59:00"):
    """
    Fetches the stock data for all S&P 500 tickers at 3:59 PM.
    Note: You can change the time to fetch the data at a different time.

    Parameters:
    - time: The time to fetch the stock data for. Default is 3:59 PM.

    Returns:
    - reshaped_dataframe: The reshaped DataFrame with the Ticker as columns and the Datetime as the index.
    """

    # Get tickers from Wikipedia
    sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].to_numpy()

    # Filter out Class B shares that have a '.B' in the ticker name
    sp500_tickers = [ticker for ticker in sp500_tickers if '.B' not in ticker]

    combined_dataframe = pd.DataFrame()

    for ticker in sp500_tickers:
        try:
            ticker_data = fetch_ticker_data(ticker, time)
            combined_dataframe = pd.concat([combined_dataframe, ticker_data])

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # Process the DataFrame
    processed_dataframe = process_dataframe(combined_dataframe)

    # Reshape the DataFrame
    reshaped_dataframe = reshape_dataframe(processed_dataframe)

    # Print Report
    print_download_report_today(combined_dataframe, sp500_tickers, time)

    return reshaped_dataframe
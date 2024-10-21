import pandas as pd
import yfinance as yf

from datetime import datetime
from utilities.print_utils import print_title, print_label, print_footer

def print_download_report(data, sp500_tickers, start_date, end_date):
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
        print_download_report(data, sp500_tickers, start_date, end_date)

    except Exception as e:
        # Handle any errors that occur during the download
        print_title(
            f"Failed to download data: {str(e)}", "bright_red", "red")
        
    return data
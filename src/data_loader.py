import yfinance as yf
import numpy as np

def fetch_1d_signal(ticker: str = "TSLA", period: str = "5d", interval: str = "1m") -> np.ndarray:
    """
    Fetches high-frequency time-series tick data from Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'TSLA', 'AAPL').
        period (str): The lookback period (e.g., '5d', '1mo').
        interval (str): The tick interval (e.g., '1m', '5m').
        
    Returns:
        np.ndarray: A flattened 1D array of the closing prices.
    """
    print(f"[*] Fetching {interval} tick data for {ticker} over the last {period}...")
    
    # Download data
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    
    if data.empty:
        raise ValueError(f"[!] No data found for ticker '{ticker}'. Check symbol or network connection.")
        
    # Extract the 'Close' prices and flatten into a 1D numpy array
    signal = data['Close'].dropna().values.flatten()
    print(f"[*] Successfully loaded {len(signal)} data points.")
    return signal
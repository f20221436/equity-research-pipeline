import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_market_data(tickers: list, start_date: str) -> pd.DataFrame:
    """Fetches historical daily market data up to the current date."""
    print(f"Initiating data pipeline for: {tickers}...")
    data_frames = []
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if df.empty:
                continue
                
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
                
            df = df.reset_index()
            df['Ticker'] = ticker
            data_frames.append(df)
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            
    if not data_frames:
        raise ValueError("Pipeline Failure: No data fetched.")
        
    return pd.concat(data_frames, ignore_index=True)
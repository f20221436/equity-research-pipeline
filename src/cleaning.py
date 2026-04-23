import pandas as pd
import logging

# Standard production logging setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans data by handling missing values, standardizing schema, and isolating anomalies."""
    logging.info("Initiating data cleaning and anomaly detection...")
    clean_df = df.copy()
    
    # Sort chronologically per ticker
    clean_df = clean_df.sort_values(by=['Ticker', 'Date']).reset_index(drop=True)
    
    # Forward fill then backward fill for missing data
    clean_df = clean_df.groupby('Ticker', group_keys=False).apply(lambda x: x.ffill().bfill())
    
    # Dynamically select price column
    price_col = 'Adj Close' if 'Adj Close' in clean_df.columns else 'Close'
    
    # --- DATA QUALITY & ANOMALY DETECTION ---
    # Calculate daily returns to check for massive, unrealistic price swings (bad data)
    clean_df['Daily_Return_Check'] = clean_df.groupby('Ticker')[price_col].pct_change()
    
    # Flag anything moving > 25% in a single day as a critical anomaly
    anomalies = clean_df[clean_df['Daily_Return_Check'].abs() > 0.25]
    
    if not anomalies.empty:
        logging.warning(f"DATA QUALITY ALERT: Flagged {len(anomalies)} extreme price anomalies (>25%).")
        # In a strict pipeline, we drop corrupted rows to protect downstream math
        clean_df = clean_df.drop(anomalies.index)
        logging.info("Corrupted anomalies successfully quarantined from the pipeline.")
    else:
        logging.info("Data Quality Check Passed: No extreme anomalies detected.")
        
    # Standardize columns for downstream features
    columns_to_keep = ['Date', 'Ticker', price_col, 'Volume']
    clean_df = clean_df[columns_to_keep]
    clean_df.rename(columns={price_col: 'Price'}, inplace=True)
    
    return clean_df
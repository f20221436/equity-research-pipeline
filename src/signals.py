import pandas as pd
import numpy as np

def generate_dynamic_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generates signals using statistical normalization and cross-sectional ranking."""
    sig_df = df.copy()
    
    # 1. Rolling Z-Score for Momentum (126 trading days ~ 6 months)
    def rolling_zscore(x):
        return (x - x.rolling(window=126).mean()) / x.rolling(window=126).std()
        
    sig_df['Momentum_Z_Score'] = sig_df.groupby('Ticker')['Momentum_1M'].transform(rolling_zscore)
    
    # 2. Cross-Sectional Ranking for Sharpe
    sig_df['Sharpe_Rank'] = sig_df.groupby('Date')['Sharpe_Ratio_30D'].rank(pct=True)
    
    # 3. Decision Logic
    condition_bullish = (sig_df['Momentum_Z_Score'] > 1.0) & (sig_df['Sharpe_Rank'] > 0.70)
    condition_bearish = (sig_df['Drawdown'] < -0.15) | (sig_df['Sharpe_Rank'] < 0.30)
    
    conditions = [condition_bullish, condition_bearish]
    choices = ['Bullish', 'Bearish']
    
    sig_df['Analyst_Signal'] = np.select(conditions, choices, default='Neutral')
    
    return sig_df.dropna(subset=['Momentum_Z_Score'])
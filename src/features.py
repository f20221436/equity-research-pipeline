import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame, risk_free_rate: float = 0.04) -> pd.DataFrame:
    """Computes risk-adjusted financial metrics per ticker."""
    feat_df = df.copy()
    daily_rf = risk_free_rate / 252

    def calculate_metrics(group):
        group['Daily_Return'] = group['Price'].pct_change()
        group['Momentum_1M'] = group['Price'].pct_change(periods=21)
        group['Volatility_30D'] = group['Daily_Return'].rolling(window=30).std() * np.sqrt(252)
        
        rolling_avg_return = group['Daily_Return'].rolling(window=30).mean()
        group['Sharpe_Ratio_30D'] = ((rolling_avg_return - daily_rf) * 252) / group['Volatility_30D']
        
        cumulative_max = group['Price'].cummax()
        group['Drawdown'] = (group['Price'] / cumulative_max) - 1
        
        return group

    feat_df = feat_df.groupby('Ticker', group_keys=False).apply(calculate_metrics)
    return feat_df.dropna()
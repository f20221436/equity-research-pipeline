from src.config import PIPELINE_CONFIG
from src.ingestion import fetch_market_data
from src.cleaning import clean_financial_data
from src.features import engineer_features
from src.signals import generate_dynamic_signals

print("🚀 Starting Local Logic Test...\n")

try:
    # 1. Ingestion
    raw = fetch_market_data(PIPELINE_CONFIG['tickers'], PIPELINE_CONFIG['start_date'])
    print(f"✔️ Ingestion passed. Raw shape: {raw.shape}")
    
    # 2. Cleaning
    clean = clean_financial_data(raw)
    print(f"✔️ Cleaning passed. Clean shape: {clean.shape}")
    
    # 3. Features
    feat = engineer_features(clean, PIPELINE_CONFIG['risk_free_rate'])
    print(f"✔️ Features passed. Feature shape: {feat.shape}")
    
    # 4. Signals
    sig = generate_dynamic_signals(feat)
    print(f"✔️ Signals passed. Final shape: {sig.shape}")
    
    print("\n✅ Pipeline executed successfully in memory. Here is the latest snapshot:")
    
    # Display the most recent day of data
    latest_date = sig['Date'].max()
    snapshot = sig[sig['Date'] == latest_date]
    print(snapshot[['Date', 'Ticker', 'Price', 'Momentum_Z_Score', 'Sharpe_Rank', 'Analyst_Signal']].to_string(index=False))

except Exception as e:
    print(f"\n❌ Pipeline failed during execution: {e}")
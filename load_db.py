from src.config import PIPELINE_CONFIG
from src.ingestion import fetch_market_data
from src.cleaning import clean_financial_data
from src.features import engineer_features
from src.signals import generate_dynamic_signals
from src.database import load_to_postgres

print("🚀 Extracting, Transforming, and Loading to PostgreSQL...\n")

try:
    # 1. Run the ETL pipeline
    raw = fetch_market_data(PIPELINE_CONFIG['tickers'], PIPELINE_CONFIG['start_date'])
    clean = clean_financial_data(raw)
    feat = engineer_features(clean, PIPELINE_CONFIG['risk_free_rate'])
    sig = generate_dynamic_signals(feat)
    
    # 2. Isolate the latest day to simulate a daily batch run
    latest_date = sig['Date'].max()
    daily_batch = sig[sig['Date'] == latest_date]
    
    print(f"\nPreparing to load {len(daily_batch)} rows for {latest_date.strftime('%Y-%m-%d')} into Postgres...")
    
    # 3. Load to Database
    load_to_postgres(daily_batch, table_name='daily_signals')
    
    print("\n✅ End-to-end pipeline execution complete!")

except Exception as e:
    print(f"\n❌ Error during execution: {e}")
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the Python path so Airflow can find your 'src' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import PIPELINE_CONFIG
from src.ingestion import fetch_market_data
from src.cleaning import clean_financial_data
from src.features import engineer_features
from src.signals import generate_dynamic_signals
from src.database import load_to_postgres

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_etl():
    raw_data = fetch_market_data(PIPELINE_CONFIG['tickers'], PIPELINE_CONFIG['start_date'])
    cleaned_data = clean_financial_data(raw_data)
    features_data = engineer_features(cleaned_data, PIPELINE_CONFIG['risk_free_rate'])
    signal_data = generate_dynamic_signals(features_data)
    
    # Isolate today's batch
    latest_date = signal_data['Date'].max()
    daily_batch = signal_data[signal_data['Date'] == latest_date]
    
    load_to_postgres(daily_batch)

with DAG(
    'equity_research_pipeline',
    default_args=default_args,
    description='Daily equity data ETL to Postgres',
    schedule_interval='0 18 * * 1-5',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    execute_etl = PythonOperator(
        task_id='run_full_etl',
        python_callable=run_etl,
    )
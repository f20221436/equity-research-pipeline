import pandas as pd
from sqlalchemy import create_engine
from src.config import get_db_connection_string

def load_to_postgres(df: pd.DataFrame, table_name: str = 'daily_signals'):
    """Loads the final DataFrame into PostgreSQL."""
    engine = create_engine(get_db_connection_string())
    
    try:
        # if_exists='append' adds daily batches to the DB
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f" Successfully loaded {len(df)} rows into '{table_name}'.")
    except Exception as e:
        print(f" Database connection or loading error: {e}")
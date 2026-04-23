import os

# Pipeline Configuration
PIPELINE_CONFIG = {
    'tickers': ['AAPL', 'MSFT', 'JPM', 'GS'],
    'start_date': '2020-01-01',
    'risk_free_rate': 0.04
}

# Database Configuration (Using environment variables for security)
DB_CONFIG = {
    'user': os.environ.get("POSTGRES_USER", "postgres"),
    'pass': os.environ.get("POSTGRES_PASSWORD", "postgres"),
    'host': os.environ.get("POSTGRES_HOST", "localhost"),
    'port': os.environ.get("POSTGRES_PORT", "5432"),
    'name': os.environ.get("POSTGRES_DB", "equity_db")
}

def get_db_connection_string():
    return f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['pass']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"
# Automated Equity Research ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.1.4-150458.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0-336791.svg)
![Airflow](https://img.shields.io/badge/Apache_Airflow-2.8.3-017CEE.svg)

## Overview
A production-grade ETL pipeline developed to automate the acquisition and analysis of equity market data. This project is designed to enhance analyst efficiency by replacing manual data processes with a scalable, modular Python library. It handles the end-to-end lifecycle of financial data, from raw ingestion to the generation of statistically defensible analyst signals.

## Key Features & JD Alignment

* **Automated Data Processes:** Built recurring Python processes to acquire and clean data sets, supporting the creation of differentiated research models.
* **Advanced Data Quality:** Implemented a robust validation layer using Pandas and NumPy to investigate data anomalies and quarantine extreme price swings (>25%).
* **Financial Market Logic:** Engineered risk-adjusted metrics including 30-day Volatility, Drawdowns, and the Sharpe Ratio to evaluate risk/return profiles.
* **Scalable Infrastructure:** Orchestrated task scheduling with Apache Airflow and maintained data integrity via a centralized PostgreSQL data warehouse.

## Project Architecture

1.  **Ingestion Layer (`src/ingestion.py`)**: Fetches historical market data for target tickers (AAPL, MSFT, JPM, GS) using the `yfinance` API.
2.  **Cleaning & DQ Layer (`src/cleaning.py`)**: standardizes schemas and implements anomaly detection logic to ensure data continuity.
3.  **Feature Engineering (`src/features.py`)**: Computes rolling quantitative metrics across partitioned time series.
4.  **Signal Generation (`src/signals.py`)**: Utilizes Rolling Z-Scores and Cross-Sectional Ranking to identify statistical outliers without relying on arbitrary fixed thresholds.
5.  **Persistence Layer (`src/database.py`)**: Loads validated analytical snapshots into a PostgreSQL database for downstream querying.

## Setup Instructions

### Prerequisites
* Python 3.10+
* PostgreSQL (Local or Docker)

### Installation
1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:f20221436/equity-research-pipeline.git
    cd equity-research-pipeline
    ```
2.  **Setup Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Execution:**
    To run the end-to-end pipeline and load data into your local Postgres instance:
    ```bash
    python load_db.py
    ```

## Author
**Amartya Kumar** BITS Pilani, Goa Campus
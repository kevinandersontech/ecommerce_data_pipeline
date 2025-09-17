# E-commerce Data Pipeline

A small but realistic data pipeline for an online store. It ingests mock order data, validates it, loads it into DuckDB, transforms it with dbt, and produces daily revenue metrics.

## Features
- Generates synthetic data for orders, items, and customers
- Runs validation checks to ensure data quality
- Loads data into a local DuckDB warehouse
- Uses dbt to build staging, facts, and marts
- Exports daily revenue metrics as CSV

## Quick Start
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run the daily pipeline
python -m pipeline.run_daily

# Backfill 30 days of history and build docs
python -m pipeline.backfill --days 30
dbt deps --project-dir dbt
dbt docs generate --project-dir dbt
```
Outputs: `warehouse/ecom.duckdb`, `exports/revenue_daily.csv`, and `dbt/target`.

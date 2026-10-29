# CommercePulse
### A Batch Data Engineering and Analytics Platform

CommercePulse is a data engineering project built using Python, Pandas, Parquet and PostgreSQL. It processes real-world e-commerce order data, validates data quality, generates monthly order analytics, and loads the results into a PostgreSQL analytics warehouse.

The project uses the Brazilian E-Commerce Public Dataset by Olist and demonstrates an end-to-end batch data pipeline.

## Project Objectives

- Build a repeatable batch data ingestion pipeline.
- Implement automated data quality validation.
- Store processed data in Parquet format.
- Generate monthly order analytics using Python and Pandas.
- Load analytical results into PostgreSQL.
- Automate pipeline execution and test core functionality.

## Architecture

```text
Olist CSV Dataset
       |
       v
Data Ingestion
       |
       v
Data Quality Validation
       |
       v
Processed Orders (Parquet)
       |
       v
Monthly Analytics (Pandas)
       |
       +----------------------+
       |                      |
       v                      v
Monthly Analytics       Data Quality Report
   (Parquet)                 (CSV)
       |
       v
PostgreSQL Analytics Warehouse
```

The pipeline is orchestrated by `run_pipeline.py`.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | Data processing and aggregation |
| PyArrow | Parquet storage support |
| PostgreSQL | Relational analytics warehouse |
| Psycopg | Python-to-PostgreSQL connectivity |
| pytest | Automated testing |
| Git | Version control |

## Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist.

The order dataset contains approximately 99,000 records with information such as:

- Order ID
- Customer ID
- Order status
- Purchase timestamp

The current dataset contains **99,441 orders**.

Download the original dataset from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

After downloading and extracting the dataset, place the required CSV files in `data/raw/`. The ingestion pipeline currently uses `olist_orders_dataset.csv`.

## Project Structure

```text
CommercePulse/
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
├── logs/
├── src/
│   ├── ingestion/
│   │   ├── load_orders.py
│   │   └── ingest_olist_orders.py
│   ├── processing/
│   │   └── build_monthly_analytics.py
│   ├── quality/
│   │   ├── validate_orders.py
│   │   └── quality_report.py
│   └── warehouse/
│       ├── __init__.py
│       └── load_monthly_analytics.py
├── sql/
├── tests/
│   ├── test_validate_orders.py
│   └── test_monthly_analytics.py
├── run_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Pipeline Workflow

### 1. Data Ingestion

Loads the raw Olist order CSV into a Pandas DataFrame and checks the dataset's structure.

### 2. Data Quality Validation

Checks for:

- Missing required columns
- Missing values in required fields
- Duplicate order IDs
- Invalid order statuses
- Invalid purchase timestamps

If validation fails, the ingestion pipeline stops instead of writing invalid orders to the processed output.

### 3. Processed Data Storage

Validated orders are written to:

`data/processed/olist_orders.parquet`

Parquet provides a columnar storage format suitable for analytical processing.

### 4. Monthly Analytics

The processing module groups orders by purchase month and order status, calculating the distinct order count for each group.

Output:

`data/warehouse/monthly_order_analytics.parquet`

### 5. Data Quality Reporting

The quality reporting module generates metrics covering total rows, unique and duplicate order IDs, missing key values, invalid statuses, invalid timestamps, and validation results.

Output:

`data/warehouse/data_quality_report.csv`

### 6. PostgreSQL Warehouse Loading

The warehouse loader reads the monthly analytics Parquet file and inserts its records into the PostgreSQL table `monthly_order_analytics`.

Existing month-and-status combinations are updated on subsequent runs, avoiding duplicate groups.

## Prerequisites

- Python 3.14 or another compatible Python version
- Ubuntu or WSL2 Ubuntu
- PostgreSQL
- Git

The commands below assume the project is run from Ubuntu or WSL2.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/rud11fadte/CommercePulse.git
cd CommercePulse
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
pip install "psycopg[binary]"
```

Download and extract the Olist dataset, then place `olist_orders_dataset.csv` in `data/raw/`.

## PostgreSQL Setup

Install PostgreSQL if it is not already installed:

```bash
sudo apt update
sudo apt install postgresql
```

Start the PostgreSQL service:

```bash
sudo pg_ctlcluster 18 main start
```

Create the database and analytics table:

```bash
sudo -u postgres psql
```

Execute these SQL statements inside the PostgreSQL prompt:

```sql
CREATE DATABASE commercepulse;
\c commercepulse

CREATE TABLE monthly_order_analytics (
    purchase_month VARCHAR(7) NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    order_count INTEGER NOT NULL CHECK (order_count >= 0),
    PRIMARY KEY (purchase_month, order_status)
);

CREATE USER commercepulse_app WITH PASSWORD 'REPLACE_WITH_A_STRONG_PASSWORD';

GRANT CONNECT ON DATABASE commercepulse TO commercepulse_app;
GRANT USAGE ON SCHEMA public TO commercepulse_app;
GRANT SELECT, INSERT, UPDATE
ON TABLE monthly_order_analytics
TO commercepulse_app;

\q
```

Use your own strong database password. Do not commit passwords or connection strings containing credentials to Git.

Configure the database connection in the terminal where you will run the application:

```bash
read -rsp "Database password: " DB_PASSWORD
echo

export COMMERCEPULSE_DATABASE_URL="postgresql://commercepulse_app:${DB_PASSWORD}@localhost:5432/commercepulse"

unset DB_PASSWORD
```

Keep this connection variable available in the terminal while running the pipeline.

## Run the Pipeline

From the project root, run:

```bash
python run_pipeline.py
```

The pipeline executes these stages in order:

1. Order ingestion and validation
2. Monthly analytics generation
3. Data quality report generation
4. PostgreSQL warehouse loading

The pipeline stops if a stage fails.

## Run Automated Tests

Execute:

```bash
python -m pytest tests/ -v
```

The current test suite contains **11 tests** covering order validation and monthly analytics.

## Query the Analytics Warehouse

Connect to PostgreSQL:

```bash
sudo -u postgres psql -d commercepulse
```

Count the analytical records:

```sql
SELECT COUNT(*) AS total_analytics_rows
FROM monthly_order_analytics;
```

Inspect monthly order counts:

```sql
SELECT purchase_month, order_status, order_count
FROM monthly_order_analytics
ORDER BY purchase_month, order_status
LIMIT 10;
```

Compare order statuses across months:

```sql
SELECT
    purchase_month,
    SUM(order_count) AS total_orders
FROM monthly_order_analytics
GROUP BY purchase_month
ORDER BY purchase_month;
```

Exit the PostgreSQL prompt with:

```sql
\q
```

## Verified Results

During local testing, the project produced the following results:

| Metric | Result |
|---|---:|
| Source orders processed | 99,441 |
| Monthly analytics groups | 136 |
| Duplicate order IDs | 0 |
| Reported validation errors | 0 |
| Automated tests passed | 11 of 11 |
| PostgreSQL analytics rows | 136 |

These results reflect the dataset and validation checks used during the recorded test runs.

## Current Scope and Limitations

CommercePulse currently implements a local batch-processing workflow. It does not yet implement a streaming ingestion system, Kafka integration, distributed Spark processing, dbt transformations, or a web dashboard.

The PostgreSQL warehouse currently stores monthly aggregated analytics rather than every source order in a relational fact table.

## Future Enhancements

- Add a PostgreSQL fact table for detailed order-level analysis.
- Add analytical dimensions for customers, products, and sellers.
- Introduce additional data quality rules and reconciliation checks.
- Add database integration tests.
- Add dbt models and documentation.
- Add a FastAPI backend and interactive analytics dashboard.
- Add continuous integration using GitHub Actions.
- Explore streaming and distributed processing where appropriate.

## Author

**Rudresh Fadate**

MSc Data Science  
Goa University

GitHub: https://github.com/rud11fadte

LinkedIn: https://www.linkedin.com/in/rudresh-fadate

---

*CommercePulse is an academic data engineering project developed for learning and demonstration purposes.*
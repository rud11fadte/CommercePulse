# CommercePulse
### End-to-End E-Commerce Data Engineering and Analytics Platform

CommercePulse is an end-to-end data engineering project that processes Brazilian e-commerce order data, validates data quality, generates monthly analytics, stores results in PostgreSQL, and exposes insights through a FastAPI backend and an interactive Streamlit dashboard.

The project uses the publicly available Brazilian E-Commerce Public Dataset by Olist.

## Project Objectives

- Build a reproducible batch data ingestion pipeline.
- Validate data quality before generating analytics.
- Transform raw order data into analytical datasets using Pandas.
- Store monthly analytics in a PostgreSQL data warehouse.
- Develop REST API endpoints using FastAPI.
- Visualize order trends and data quality through Streamlit.
- Containerize the application using Docker and Docker Compose.
- Implement automated testing for important pipeline components.

## Architecture

```text
                    Olist Raw CSV Dataset
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
                 +-----------+-----------+
                 |                       |
                 v                       v
         Monthly Analytics         Quality Report
             (Parquet)                 (CSV)
                 |
                 v
          PostgreSQL Warehouse
                 |
                 v
              FastAPI
                 |
                 v
         Streamlit Dashboard

       Docker Compose orchestrates
       the application services.
```

The `run_pipeline.py` script coordinates the batch pipeline, while Docker Compose manages PostgreSQL, the pipeline, the API, and the dashboard.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline and application logic |
| Pandas | Data transformation and aggregation |
| PyArrow | Parquet data storage |
| PostgreSQL | Analytical data warehouse |
| SQL | Database schema and analytical queries |
| FastAPI | REST API development |
| Pydantic | API data validation |
| Streamlit | Interactive analytics dashboard |
| Plotly | Interactive visualizations |
| Requests | API communication from the dashboard |
| Pytest | Automated testing |
| HTTPX | API testing |
| Docker | Application containerization |
| Docker Compose | Multi-service orchestration |
| Git and GitHub | Version control and project hosting |

## Dataset

CommercePulse uses the Brazilian E-Commerce Public Dataset by Olist.

The dataset contains information about orders placed on the Olist e-commerce platform in Brazil.

**Dataset source:**
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The current pipeline processes the order dataset:

`olist_orders_dataset.csv`

The raw dataset is stored locally and is excluded from Git tracking because of its size.

### Dataset Fields

Important order attributes include:

- `order_id` — Unique identifier for an order.
- `customer_id` — Identifier for the customer.
- `order_status` — Current order status.
- `order_purchase_timestamp` — Timestamp when the order was purchased.
- `order_approved_at` — Timestamp when the order was approved.
- `order_delivered_carrier_date` — Timestamp when the order was handed to the carrier.
- `order_delivered_customer_date` — Timestamp when the order was delivered.
- `order_estimated_delivery_date` — Estimated delivery timestamp.

## Project Structure

```text
CommercePulse/
|
|-- app/
|   |-- dashboard.py
|
|-- data/
|   |-- raw/
|   |-- processed/
|   |-- warehouse/
|
|-- logs/
|
|-- sql/
|   |-- init.sql
|
|-- src/
|   |-- api/
|   |   |-- main.py
|   |
|   |-- ingestion/
|   |   |-- load_orders.py
|   |   |-- ingest_olist_orders.py
|   |
|   |-- processing/
|   |   |-- build_monthly_analytics.py
|   |
|   |-- quality/
|   |   |-- validate_orders.py
|   |   |-- quality_report.py
|   |
|   |-- warehouse/
|       |-- load_monthly_analytics.py
|
|-- tests/
|   |-- test_validate_orders.py
|   |-- test_monthly_analytics.py
|   |-- test_api.py
|
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
|-- run_pipeline.py
|-- README.md
```

## Data Engineering Pipeline

CommercePulse implements a batch processing workflow with the following stages.

### 1. Data Ingestion

The ingestion module reads the raw Olist order dataset and performs initial checks.

Responsibilities include:

- Loading order records from CSV.
- Checking required columns.
- Preparing data for validation.
- Logging ingestion results.
- Saving validated orders in Parquet format.

Output:

`data/processed/olist_orders.parquet`

### 2. Data Quality Validation

The validation module checks the order dataset for common data quality problems.

Checks include:

- Missing required fields.
- Duplicate order identifiers.
- Invalid order statuses.
- Invalid timestamps.
- Missing critical identifiers.

The pipeline records validation results and reports data quality errors.

### 3. Monthly Analytics

The processing module groups order records by purchase month and order status.

It calculates the number of orders in each group and produces a monthly analytical dataset.

Output:

`data/warehouse/monthly_order_analytics.parquet`

The current dataset produces 136 monthly and order-status aggregation rows.

### 4. Data Quality Reporting

The quality reporting module generates a CSV report containing important quality metrics, including:

- Total number of rows.
- Number of unique order identifiers.
- Duplicate order identifiers.
- Missing critical values.
- Invalid statuses.
- Invalid timestamps.
- Total validation errors.
- Overall validation result.

Output:

`data/warehouse/data_quality_report.csv`

### 5. PostgreSQL Warehouse

The warehouse module loads monthly analytics into PostgreSQL.

The table `monthly_order_analytics` stores:

- `purchase_month`
- `order_status`
- `order_count`

The table uses a composite primary key consisting of `purchase_month` and `order_status`.

The loading process supports upserts, allowing existing monthly aggregates to be updated when the pipeline is rerun.

### 6. Pipeline Orchestration

The `run_pipeline.py` script executes the pipeline stages in sequence.

It coordinates ingestion and validation, monthly analytics generation, quality reporting, and PostgreSQL loading.

## REST API

CommercePulse uses FastAPI to expose analytical data through REST endpoints.

### Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API and database health |
| GET | `/analytics/monthly` | Retrieves monthly order analytics |
| GET | `/analytics/monthly?month=2017-01` | Filters analytics by month |
| GET | `/analytics/monthly?status=delivered` | Filters analytics by order status |
| GET | `/analytics/quality` | Retrieves the data quality report |

Month and status filters can be combined.

### Example Response

A request to `/analytics/monthly` returns a JSON response containing a record count and analytical data.

```json
{
  "count": 2,
  "data": [
    {
      "purchase_month": "2017-01",
      "order_status": "delivered",
      "order_count": 120
    },
    {
      "purchase_month": "2017-01",
      "order_status": "shipped",
      "order_count": 15
    }
  ]
}
```

The values above are illustrative examples, not the actual query results.

### API Documentation

When the application is running, interactive API documentation is available at:

http://localhost:8000/docs

## Streamlit Analytics Dashboard

CommercePulse includes an interactive dashboard built with Streamlit and Plotly.

The dashboard communicates with the FastAPI backend to retrieve analytical results.

### Dashboard Features

- Monthly and order-status filters.
- Key performance indicator cards.
- Monthly order trend visualization.
- Order counts by status.
- Data quality monitoring.
- Validation status and error metrics.
- Expandable data quality report.
- Monthly analytics table.

The dashboard provides a convenient interface for exploring the results of the data pipeline without manually querying the database.

### Access the Dashboard

http://localhost:8501

## Docker Deployment

Docker Compose manages the application's services.

| Service | Purpose |
|---|---|
| PostgreSQL | Stores monthly analytical aggregates |
| Pipeline | Runs the batch data processing workflow |
| FastAPI | Serves analytics and health endpoints |
| Streamlit | Displays the analytics dashboard |

The PostgreSQL container uses a named Docker volume for persistent database storage.

The raw dataset and generated data are mounted from the local project directory rather than committed to GitHub.

### Prerequisites

- Docker Desktop or Docker Engine with Docker Compose.
- Git.
- The Olist order dataset downloaded to the project's `data/raw/` directory.

### Environment Configuration

The repository includes `.env.example` as a template for the database password.

Create your local `.env` file from the project root:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder with a strong, randomly generated password.

Keep `.env` private and never commit it to GitHub.

### Run the Pipeline

Build the image and execute the batch pipeline:

```bash
docker compose run --build --rm pipeline
```

### Start the Services

Start PostgreSQL, the API, and the dashboard:

```bash
docker compose up -d postgres api dashboard
```

If the pipeline has not been executed yet, run it before using the dashboard.

### Check Running Containers

```bash
docker compose ps
```

The pipeline is a one-shot job, so it will not necessarily appear in the running-container list after it finishes.

### View Logs

```bash
docker compose logs -f postgres api dashboard
```

### Stop the Services

```bash
docker compose down
```

The named PostgreSQL volume is preserved when the containers are stopped this way.

To delete the database volume and its stored data, use the following command only when you intentionally want to reset the database:

```bash
docker compose down -v
```

## Local Development

Docker is the recommended way to run the complete application.

For local Python development, create and activate a virtual environment from the project root.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the automated tests:

```bash
pytest -v
```

Run the pipeline locally after configuring a reachable PostgreSQL database and setting the required database connection environment variable:

```bash
python run_pipeline.py
```

Start the API locally:

```bash
uvicorn src.api.main:app --reload
```

Start the dashboard locally in a separate terminal:

```bash
streamlit run app/dashboard.py
```

For local execution, ensure that the API and dashboard configuration points to the correct service URLs and that the PostgreSQL connection settings are configured appropriately.

## Results and Current Implementation

The pipeline has been tested against the local Olist order dataset.

| Metric | Result |
|---|---:|
| Orders processed | 99,441 |
| Unique order identifiers | 99,441 |
| Duplicate order identifiers | 0 |
| Monthly analytics rows | 136 |
| PostgreSQL analytics rows | 136 |
| Validation errors | 0 |
| Overall validation result | Passed |

These results describe the current processed dataset and may change if the source data changes.

## Testing

CommercePulse includes automated tests for core functionality.

### Order Validation Tests

The validation tests cover data quality rules such as missing fields, duplicate identifiers, invalid statuses, and timestamps.

### Monthly Analytics Tests

The analytics tests verify monthly aggregation logic and expected output structure.

### API Tests

The API tests validate endpoint behavior, response structure, and relevant error-handling scenarios.

Run the test suite using:

```bash
pytest -v
```

## Security and Data Management

- Database credentials are supplied through environment variables.
- The local `.env` file is excluded from version control.
- The PostgreSQL port is bound to the local machine.
- The raw dataset is excluded from Git tracking.
- Generated data, logs, and virtual environments are excluded from Git tracking.
- Docker containers are used to isolate the application services.

For production deployment, additional controls would be required, including authentication, authorization, HTTPS, secrets management, and production-grade monitoring.

## Current Limitations

- The pipeline currently focuses on batch processing rather than real-time streaming.
- Analytics are based on order counts grouped by purchase month and status.
- The dashboard depends on the API and the generated analytical data.
- The current implementation does not include user authentication.
- The quality report is generated as a local CSV file.
- The project is designed for educational and demonstration purposes rather than production-scale operations.

## Future Enhancements

Potential improvements include:

- Scheduling automated pipeline execution.
- Adding Apache Airflow for workflow orchestration.
- Introducing Apache Kafka for event-driven ingestion.
- Implementing incremental ingestion and processing.
- Expanding analytics to revenue, delivery performance, and customer behavior.
- Adding more detailed data quality rules and historical quality tracking.
- Adding API authentication and role-based access control.
- Implementing CI/CD with GitHub Actions.
- Adding automated monitoring and alerting.
- Deploying the application to a cloud platform.

## Learning Outcomes

This project demonstrates practical experience with:

- Batch data engineering.
- Data ingestion and transformation.
- Data quality validation.
- Columnar storage using Parquet.
- Relational database design and upserts.
- REST API development.
- Interactive analytics dashboards.
- Automated testing.
- Containerization and multi-service deployment.
- Version control and project documentation.

## Author

**Rudresh Mahendra Fadate**

MSc Data Science
Goa Business School, Goa University

GitHub: https://github.com/rud11fadte

## Acknowledgements

Dataset: Brazilian E-Commerce Public Dataset by Olist.

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

---

CommercePulse — From raw e-commerce data to validated, accessible, and interactive analytics.

# 📊 CommercePulse

### E-commerce Data Engineering and Analytics Platform

CommercePulse is an end-to-end data engineering and analytics project built using Python, Pandas, PostgreSQL, FastAPI, Streamlit and Docker.

The project processes Brazilian e-commerce order data, performs data validation, generates monthly analytical datasets, stores results in a PostgreSQL warehouse and presents business insights through an interactive dashboard.

**Live Dashboard:** https://commercepulse-bdnpe7tm9frg4pbrmscmxf.streamlit.app

**GitHub Repository:** https://github.com/rud11fadte/CommercePulse

---

## 🚀 Project Overview

CommercePulse demonstrates a practical data engineering workflow, from raw data ingestion to analytics and visualization.

The platform is designed around the following stages:

1. **Data Ingestion** – Load raw e-commerce order data.
2. **Data Validation** – Identify missing values, duplicate IDs, invalid statuses and timestamp issues.
3. **Data Processing** – Transform order data into monthly analytical datasets.
4. **Data Quality Reporting** – Generate a report containing validation metrics.
5. **Data Warehousing** – Load processed analytics into PostgreSQL.
6. **API Development** – Expose analytics through FastAPI endpoints.
7. **Data Visualization** – Present insights through an interactive Streamlit dashboard.
8. **Cloud Deployment** – Publish the dashboard using Streamlit Community Cloud.

---

## 🏗️ Architecture

### Local data engineering architecture

```text
              Olist E-commerce Dataset
                         |
                         v
                 Data Ingestion
                         |
                         v
                Data Validation
                         |
                         v
                Data Processing
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Monthly Analytics       Data Quality Report
             |                       |
             +-----------+-----------+
                         |
                         v
                 PostgreSQL
                  Warehouse
                         |
                         v
                    FastAPI
                         |
                         v
                Streamlit Dashboard
```

### Cloud dashboard architecture

The public Streamlit dashboard uses precomputed analytics files stored in the GitHub repository.

```text
       Data Pipeline (Local)
                |
                v
       Monthly Analytics
         (Parquet File)
                |
                v
       Data Quality Report
           (CSV File)
                |
                v
          GitHub Repository
                |
                v
      Streamlit Community Cloud
                |
                v
       Public CommercePulse
             Dashboard
```

The cloud dashboard reads these files directly. It does not depend on the local FastAPI server or PostgreSQL database being online.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Data Storage | PostgreSQL |
| Data Format | CSV, Parquet |
| API Development | FastAPI |
| API Server | Uvicorn |
| Visualization | Streamlit, Plotly |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Testing | Pytest |
| Version Control | Git, GitHub |
| Cloud Dashboard Hosting | Streamlit Community Cloud |

---

## 📂 Dataset

CommercePulse uses the public Brazilian E-Commerce Public Dataset by Olist.

The dataset contains information about e-commerce orders, customers, payments, products, sellers and deliveries.

The project primarily uses order information to demonstrate data ingestion, validation and monthly analytics.

**Dataset:** Olist Brazilian E-Commerce Dataset

The original raw dataset is maintained locally and is excluded from GitHub to avoid committing large source files.

---

## ⚙️ Data Engineering Pipeline

The pipeline is orchestrated through `run_pipeline.py`.

### 1. Data Ingestion

- Reads raw order data from CSV files.
- Loads order records into the processing workflow.
- Handles the source order dataset.

### 2. Data Quality Validation

The validation module checks:

- Missing order IDs.
- Duplicate order IDs.
- Missing customer IDs.
- Missing order statuses.
- Invalid order statuses.
- Invalid purchase timestamps.

### 3. Monthly Analytics

The processing module aggregates orders by:

- Purchase month.
- Order status.
- Number of orders.

The generated monthly analytics dataset is stored in Parquet format.

### 4. Data Quality Reporting

A data quality report is generated with metrics such as:

- Total source rows.
- Unique order IDs.
- Duplicate order IDs.
- Missing order IDs.
- Missing customer IDs.
- Missing order statuses.
- Invalid order statuses.
- Invalid purchase timestamps.
- Validation error count.
- Validation status.

### 5. PostgreSQL Warehouse

The processed monthly analytics are loaded into PostgreSQL using the warehouse loading module.

---

## 📊 Project Results

Results from the current processed dataset:

| Metric | Result |
|---|---:|
| Total source orders | 99,441 |
| Unique order IDs | 99,441 |
| Duplicate order IDs | 0 |
| Validation errors | 0 |
| Monthly analytics records | 136 |
| Months represented | 25 |
| Order statuses | 8 |
| Data validation | Passed |

These figures represent the current processed dataset snapshot.

---

## 📈 Interactive Dashboard

The CommercePulse dashboard is built using Streamlit and Plotly.

### Dashboard Features

**Business Overview**
- Total orders in the selected dataset.
- Number of months represented.
- Number of order statuses.

**Interactive Filters**
- Filter by purchase month.
- Filter by order status.
- Dynamically update dashboard metrics and charts.

**Visual Analytics**
- Monthly order trends.
- Order status distribution.

**Data Quality Monitoring**
- Data validation status.
- Total source rows.
- Unique order IDs.
- Duplicate order IDs.
- Validation errors.
- Complete quality report.

### Live Dashboard

🌐 **[Open CommercePulse Dashboard](https://commercepulse-bdnpe7tm9frg4pbrmscmxf.streamlit.app)**

The dashboard is publicly accessible through Streamlit Community Cloud.

Note: Streamlit Community Cloud may put inactive applications to sleep. The application can take some time to wake up when a visitor opens it.

---

## 🔌 FastAPI Endpoints

The project also includes a FastAPI service for accessing analytical data.

When running the local Docker deployment, the API is available at:

`http://localhost:8000`

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Check API and database health |
| `/analytics/monthly` | GET | Retrieve monthly order analytics |
| `/analytics/quality` | GET | Retrieve the data quality report |
| `/docs` | GET | Interactive API documentation |

Interactive API documentation:

`http://localhost:8000/docs`

The public Streamlit dashboard currently reads its committed analytics files directly rather than calling these endpoints.

---

## 🐳 Run Locally Using Docker

### Prerequisites

- Git
- Docker Desktop
- Docker Compose
- Windows with WSL2, Linux or macOS

### 1. Clone the repository

```bash
git clone https://github.com/rud11fadte/CommercePulse.git

cd CommercePulse
```

### 2. Configure environment variables

Create your local environment file:

```bash
cp .env.example .env
```

Configure the required PostgreSQL settings in `.env`.

Do not commit your `.env` file to GitHub.

### 3. Start the application

```bash
docker compose up --build -d
```

Docker Compose starts the required services:

- PostgreSQL database.
- Data pipeline.
- FastAPI application.
- Streamlit dashboard.

The pipeline runs as a one-time job and exits after successful execution.

### 4. Access the services

| Service | Local URL |
|---|---|
| Streamlit Dashboard | http://localhost:8501 |
| FastAPI | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| PostgreSQL | localhost:5433 |

### 5. Check running containers

```bash
docker compose ps
```

### 6. View application logs

```bash
docker compose logs -f
```

### 7. Stop the application

```bash
docker compose down
```

To remove containers and the PostgreSQL volume:

```bash
docker compose down -v
```

Warning: Removing the volume deletes the persisted local database data.

---

## 🐍 Run the Pipeline Manually

If you prefer running the data pipeline outside Docker:

### 1. Clone the repository

```bash
git clone https://github.com/rud11fadte/CommercePulse.git

cd CommercePulse
```

### 2. Create a virtual environment

Linux / WSL:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Windows:

```powershell
py -m venv .venv

.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Configure the PostgreSQL connection settings as required.

### 5. Run the pipeline

```bash
python run_pipeline.py
```

The pipeline performs ingestion, validation, analytics generation, quality reporting and warehouse loading.

---

## ☁️ Streamlit Community Cloud Deployment

CommercePulse is deployed using Streamlit Community Cloud.

### Deployment configuration

| Setting | Value |
|---|---|
| Hosting Platform | Streamlit Community Cloud |
| Repository | `rud11fadte/CommercePulse` |
| Branch | `main` |
| Main File | `app/dashboard.py` |
| Python Version | 3.12 |
| Dashboard URL | `https://commercepulse-bdnpe7tm9frg4pbrmscmxf.streamlit.app` |

### Dashboard data files

The cloud dashboard reads these files directly:

```text
app/
├── dashboard.py
└── data/
    ├── monthly_order_analytics.parquet
    └── data_quality_report.csv
```

This makes the deployed dashboard independent of local API and database services.

### Updating the cloud dashboard

When the pipeline generates new analytics:

1. Update the dashboard data files.
2. Commit the updated files to GitHub.
3. Push the changes to the `main` branch.
4. Streamlit Community Cloud detects the changes and redeploys the application.

Example:

```bash
git add app/dashboard.py app/data/

git commit -m "Update dashboard analytics"

git push origin main
```

---

## 🧪 Testing

The project includes automated tests for data validation, monthly analytics and API functionality.

Run the test suite:

```bash
pytest -v
```

The test suite previously completed with 16 passing tests.

Tests cover:

- Order data validation.
- Monthly analytics calculations.
- API endpoint behaviour.

---

## 📁 Project Structure

```text
CommercePulse/
│
├── app/
│   ├── dashboard.py
│   └── data/
│       ├── monthly_order_analytics.parquet
│       └── data_quality_report.csv
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
│
├── src/
│   ├── ingestion/
│   │   ├── load_orders.py
│   │   └── ingest_olist_orders.py
│   │
│   ├── quality/
│   │   ├── validate_orders.py
│   │   └── quality_report.py
│   │
│   ├── processing/
│   │   └── build_monthly_analytics.py
│   │
│   ├── warehouse/
│   │   └── load_monthly_analytics.py
│   │
│   └── api/
│       └── main.py
│
├── sql/
│   └── init.sql
│
├── tests/
│   ├── test_validate_orders.py
│   ├── test_monthly_analytics.py
│   └── test_api.py
│
├── run_pipeline.py
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── Dockerfile.api
├── Dockerfile.render
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔮 Future Improvements

Potential improvements for future development:

- Automated scheduled data ingestion.
- Incremental data processing.
- Real-time order analytics.
- Additional business intelligence KPIs.
- Customer segmentation and behavioural analytics.
- Advanced forecasting and predictive analytics.
- Automated cloud data pipeline execution.
- Enhanced monitoring and alerting.

---

## 👨‍💻 Author

**Rudresh Mahendra Fadate**

MSc Data Science  
Goa University, Goa Business School

GitHub: [@rud11fadte](https://github.com/rud11fadte)

Project: [CommercePulse](https://github.com/rud11fadte/CommercePulse)

---

## 📜 License

This project is developed for academic and educational purposes.

---

⭐ If you find this project useful, consider giving the repository a star!

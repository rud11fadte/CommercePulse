"""CommercePulse REST API for analytics and data quality."""

import os
from pathlib import Path

import pandas as pd
import psycopg
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="CommercePulse API",
    description="E-commerce analytics and data quality API.",
    version="1.0.0",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUALITY_REPORT = PROJECT_ROOT / "data" / "warehouse" / "data_quality_report.csv"


def get_database_url() -> str:
    url = os.getenv("COMMERCEPULSE_DATABASE_URL")
    if not url:
        raise HTTPException(
            status_code=503,
            detail="Database connection is not configured.",
        )
    return url


@app.get("/health", tags=["Health"])
def health():
    """Check API and database connectivity."""
    try:
        with psycopg.connect(get_database_url(), connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "healthy", "database": "connected"}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable.",
        ) from exc


@app.get("/analytics/monthly", tags=["Analytics"])
def monthly_analytics(
    month: str | None = Query(
        default=None,
        pattern=r"^\d{4}-(0[1-9]|1[0-2])$",
        description="Optional month filter, e.g. 2018-01",
    ),
    status: str | None = Query(default=None, description="Optional order status"),
):
    """Return monthly order counts from PostgreSQL."""
    query = """
        SELECT purchase_month, order_status, order_count
        FROM monthly_order_analytics
    """
    conditions = []
    params = []

    if month:
        conditions.append("purchase_month = %s")
        params.append(month)

    if status:
        conditions.append("order_status = %s")
        params.append(status.lower())

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY purchase_month, order_status"

    try:
        with psycopg.connect(get_database_url(), connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()

        return {
            "count": len(rows),
            "data": [
                {
                    "purchase_month": row[0],
                    "order_status": row[1],
                    "order_count": row[2],
                }
                for row in rows
            ],
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve monthly analytics.",
        ) from exc


@app.get("/analytics/quality", tags=["Data Quality"])
def data_quality():
    """Return the latest generated data quality report."""
    if not QUALITY_REPORT.exists():
        raise HTTPException(
            status_code=404,
            detail="Quality report not found. Run the pipeline first.",
        )

    try:
        report = pd.read_csv(QUALITY_REPORT, dtype=str).fillna("")
        metrics = dict(zip(report["metric"], report["value"]))

        return {
            "report": metrics,
            "report_path": "data/warehouse/data_quality_report.csv",
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to read the data quality report.",
        ) from exc

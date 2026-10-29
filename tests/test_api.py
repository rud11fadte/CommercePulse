"""Automated tests for the CommercePulse REST API."""

from unittest.mock import MagicMock

import pandas as pd
from fastapi.testclient import TestClient

from src.api import main


client = TestClient(main.app)


def configure_test_database(monkeypatch):
    monkeypatch.setenv(
        "COMMERCEPULSE_DATABASE_URL",
        "postgresql://test:test@localhost:5432/test",
    )


def mock_database(monkeypatch, rows=None):
    connection = MagicMock()
    cursor = MagicMock()
    cursor.fetchall.return_value = rows or []

    connection.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(
        main.psycopg, "connect", lambda *args, **kwargs: connection
    )
    return connection, cursor


def test_health_endpoint(monkeypatch):
    configure_test_database(monkeypatch)
    connection, cursor = mock_database(monkeypatch)
    cursor.fetchone.return_value = (1,)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
    }


def test_monthly_analytics_endpoint(monkeypatch):
    configure_test_database(monkeypatch)
    mock_database(
        monkeypatch,
        [
            ("2018-01", "delivered", 7069),
            ("2018-01", "canceled", 34),
        ],
    )

    response = client.get("/analytics/monthly?month=2018-01")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["data"][0] == {
        "purchase_month": "2018-01",
        "order_status": "delivered",
        "order_count": 7069,
    }


def test_monthly_analytics_rejects_invalid_month():
    response = client.get("/analytics/monthly?month=2018-13")
    assert response.status_code == 422


def test_quality_endpoint(monkeypatch, tmp_path):
    report_path = tmp_path / "data_quality_report.csv"
    pd.DataFrame(
        [
            {"metric": "total_rows", "value": 99441},
            {"metric": "validation_passed", "value": True},
        ]
    ).to_csv(report_path, index=False)

    monkeypatch.setattr(main, "QUALITY_REPORT", report_path)

    response = client.get("/analytics/quality")

    assert response.status_code == 200
    report = response.json()["report"]
    assert report["total_rows"] == "99441"
    assert report["validation_passed"] == "True"


def test_quality_endpoint_when_report_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(
        main, "QUALITY_REPORT", tmp_path / "missing_report.csv"
    )

    response = client.get("/analytics/quality")
    assert response.status_code == 404

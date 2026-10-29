
"""Automated tests for CommercePulse monthly analytics."""

import pandas as pd

from src.processing.build_monthly_analytics import (
    build_monthly_analytics,
)


def sample_orders():
    return pd.DataFrame(
        [
            {
                "order_id": "ORD001",
                "order_status": "delivered",
                "order_purchase_timestamp": "2018-01-10 10:00:00",
            },
            {
                "order_id": "ORD002",
                "order_status": "delivered",
                "order_purchase_timestamp": "2018-01-15 12:30:00",
            },
            {
                "order_id": "ORD003",
                "order_status": "canceled",
                "order_purchase_timestamp": "2018-01-20 14:00:00",
            },
            {
                "order_id": "ORD004",
                "order_status": "delivered",
                "order_purchase_timestamp": "2018-02-05 09:00:00",
            },
        ]
    )


def test_monthly_order_counts():
    result = build_monthly_analytics(sample_orders())

    january_delivered = result[
        (result["purchase_month"] == "2018-01")
        & (result["order_status"] == "delivered")
    ]

    assert len(january_delivered) == 1
    assert january_delivered.iloc[0]["order_count"] == 2


def test_all_orders_are_accounted_for():
    result = build_monthly_analytics(sample_orders())

    assert result["order_count"].sum() == 4


def test_month_status_groups_are_unique():
    result = build_monthly_analytics(sample_orders())

    assert not result.duplicated(
        ["purchase_month", "order_status"]
    ).any()


def test_invalid_timestamp_fails():
    orders = sample_orders()
    orders.loc[0, "order_purchase_timestamp"] = "not-a-date"

    try:
        build_monthly_analytics(orders)
    except ValueError as error:
        assert "Invalid purchase timestamps" in str(error)
    else:
        raise AssertionError("Expected invalid timestamp to fail")


def test_missing_column_fails():
    orders = sample_orders().drop(columns=["order_status"])

    try:
        build_monthly_analytics(orders)
    except ValueError as error:
        assert "Missing required columns" in str(error)
    else:
        raise AssertionError("Expected missing column to fail")

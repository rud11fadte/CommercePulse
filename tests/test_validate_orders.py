
"""Automated tests for CommercePulse Olist order validation."""

import pandas as pd

from src.quality.validate_orders import validate_orders


def valid_orders():
    return pd.DataFrame(
        [
            {
                "order_id": "ORD001",
                "customer_id": "CUST001",
                "order_status": "delivered",
                "order_purchase_timestamp": "2018-01-10 10:00:00",
            },
            {
                "order_id": "ORD002",
                "customer_id": "CUST002",
                "order_status": "shipped",
                "order_purchase_timestamp": "2018-02-15 12:30:00",
            },
        ]
    )


def test_valid_orders_pass():
    assert validate_orders(valid_orders()) == []


def test_duplicate_order_ids_fail():
    orders = valid_orders()
    orders.loc[1, "order_id"] = "ORD001"

    errors = validate_orders(orders)

    assert any("Duplicate order IDs" in error for error in errors)


def test_missing_required_value_fails():
    orders = valid_orders()
    orders.loc[0, "customer_id"] = None

    errors = validate_orders(orders)

    assert any("missing values" in error for error in errors)


def test_invalid_order_status_fails():
    orders = valid_orders()
    orders.loc[0, "order_status"] = "unknown_status"

    errors = validate_orders(orders)

    assert any("Invalid order statuses" in error for error in errors)


def test_invalid_purchase_timestamp_fails():
    orders = valid_orders()
    orders.loc[0, "order_purchase_timestamp"] = "not-a-date"

    errors = validate_orders(orders)

    assert any("purchase timestamps" in error for error in errors)


def test_missing_required_column_fails():
    orders = valid_orders().drop(columns=["customer_id"])

    errors = validate_orders(orders)

    assert any("Missing required columns" in error for error in errors)

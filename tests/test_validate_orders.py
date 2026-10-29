
"""Automated tests for CommercePulse order validation."""

import pandas as pd

from src.quality.validate_orders import validate_orders


def valid_orders():
    return pd.DataFrame(
        [
            {
                "order_id": "ORD001",
                "customer_id": "CUST001",
                "product_id": "PROD101",
                "quantity": 2,
                "unit_price": 499.00,
            },
            {
                "order_id": "ORD002",
                "customer_id": "CUST002",
                "product_id": "PROD102",
                "quantity": 1,
                "unit_price": 899.00,
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


def test_negative_quantity_fails():
    orders = valid_orders()
    orders.loc[0, "quantity"] = -1

    errors = validate_orders(orders)

    assert any("Quantity" in error for error in errors)


def test_negative_price_fails():
    orders = valid_orders()
    orders.loc[0, "unit_price"] = -10

    errors = validate_orders(orders)

    assert any("Unit price" in error for error in errors)


def test_missing_required_column_fails():
    orders = valid_orders().drop(columns=["customer_id"])

    errors = validate_orders(orders)

    assert any("Missing required columns" in error for error in errors)

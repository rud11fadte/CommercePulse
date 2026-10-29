
"""CommercePulse: order-data quality validation."""

import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
]


def validate_orders(orders: pd.DataFrame) -> list[str]:
    """Return a list of data-quality errors."""
    errors = []

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in orders.columns
    ]

    if missing_columns:
        return [f"Missing required columns: {missing_columns}"]

    if orders[REQUIRED_COLUMNS].isnull().any().any():
        errors.append("Required columns contain missing values.")

    if orders["order_id"].duplicated().any():
        errors.append("Duplicate order IDs found.")

    quantity = pd.to_numeric(orders["quantity"], errors="coerce")
    if quantity.isnull().any() or (quantity <= 0).any():
        errors.append("Quantity must be a positive number.")

    price = pd.to_numeric(orders["unit_price"], errors="coerce")
    if price.isnull().any() or (price < 0).any():
        errors.append("Unit price must be a non-negative number.")

    return errors

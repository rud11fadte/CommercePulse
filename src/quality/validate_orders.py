
"""CommercePulse: order-data quality validation."""

import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
]

VALID_ORDER_STATUSES = {
    "approved",
    "canceled",
    "created",
    "delivered",
    "invoiced",
    "processing",
    "shipped",
    "unavailable",
}


def validate_orders(orders: pd.DataFrame) -> list[str]:
    """Return a list of data-quality errors."""
    errors = []

    # Check that all required columns exist.
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in orders.columns
    ]

    if missing_columns:
        return [f"Missing required columns: {missing_columns}"]

    # Check for missing values in required columns.
    if orders[REQUIRED_COLUMNS].isnull().any().any():
        errors.append("Required columns contain missing values.")

    # Check for duplicate order IDs.
    if orders["order_id"].duplicated().any():
        errors.append("Duplicate order IDs found.")

    # Check that order statuses are recognized.
    invalid_statuses = ~orders["order_status"].isin(
        VALID_ORDER_STATUSES
    )

    if invalid_statuses.any():
        errors.append("Invalid order statuses found.")

    # Validate Olist purchase timestamps.
    purchase_dates = pd.to_datetime(
        orders["order_purchase_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    if purchase_dates.isnull().any():
        errors.append("Invalid or missing purchase timestamps.")

    return errors

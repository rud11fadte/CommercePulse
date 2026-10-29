
"""CommercePulse: generate a data quality report for order data."""

from pathlib import Path

import pandas as pd

from src.quality.validate_orders import validate_orders


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
REPORT_DIR = PROJECT_ROOT / "data" / "warehouse"
REPORT_FILE = REPORT_DIR / "data_quality_report.csv"


def generate_quality_report(orders: pd.DataFrame) -> pd.DataFrame:
    """Summarize key data quality checks for an orders dataset."""
    required_columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in orders.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot generate report. Missing columns: {missing_columns}"
        )

    validation_errors = validate_orders(orders)

    purchase_dates = pd.to_datetime(
        orders["order_purchase_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    metrics = [
        ("total_rows", len(orders)),
        ("unique_order_ids", orders["order_id"].nunique()),
        ("duplicate_order_ids", int(orders["order_id"].duplicated().sum())),
        (
            "missing_order_ids",
            int(orders["order_id"].isnull().sum()),
        ),
        (
            "missing_customer_ids",
            int(orders["customer_id"].isnull().sum()),
        ),
        (
            "missing_order_statuses",
            int(orders["order_status"].isnull().sum()),
        ),
        (
            "invalid_order_statuses",
            int(
                (
                    ~orders["order_status"].isin(
                        {
                            "approved",
                            "canceled",
                            "created",
                            "delivered",
                            "invoiced",
                            "processing",
                            "shipped",
                            "unavailable",
                        }
                    )
                ).sum()
            ),
        ),
        (
            "invalid_purchase_timestamps",
            int(purchase_dates.isnull().sum()),
        ),
        ("validation_error_count", len(validation_errors)),
        (
            "validation_passed",
            len(validation_errors) == 0,
        ),
    ]

    return pd.DataFrame(metrics, columns=["metric", "value"])


def main() -> None:
    """Generate and save the data quality report."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_FILE}")

    orders = pd.read_csv(RAW_FILE)
    report = generate_quality_report(orders)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report.to_csv(REPORT_FILE, index=False)

    print("CommercePulse data quality report generated.")
    print(f"Rows analysed: {len(orders):,}")
    print(f"Report saved to: {REPORT_FILE}")
    print("\nQuality metrics:")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()

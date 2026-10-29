
"""CommercePulse: build monthly order analytics."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "olist_orders.parquet"
OUTPUT_DIR = PROJECT_ROOT / "data" / "warehouse"
OUTPUT_FILE = OUTPUT_DIR / "monthly_order_analytics.parquet"


def build_monthly_analytics(orders: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order counts by purchase month and order status."""
    required_columns = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
    ]

    missing = [
        column for column in required_columns
        if column not in orders.columns
    ]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = orders[required_columns].copy()

    data["purchase_timestamp"] = pd.to_datetime(
        data["order_purchase_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    if data["purchase_timestamp"].isnull().any():
        raise ValueError("Invalid purchase timestamps found.")

    data["purchase_month"] = (
        data["purchase_timestamp"].dt.to_period("M").astype(str)
    )

    analytics = (
        data.groupby(
            ["purchase_month", "order_status"],
            as_index=False,
        )
        .agg(order_count=("order_id", "nunique"))
        .sort_values(["purchase_month", "order_status"])
        .reset_index(drop=True)
    )

    return analytics


def main() -> None:
    """Read validated orders and save the monthly analytics table."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input not found: {INPUT_FILE}. Run the ingestion pipeline first."
        )

    orders = pd.read_parquet(INPUT_FILE)
    analytics = build_monthly_analytics(orders)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    analytics.to_parquet(OUTPUT_FILE, index=False)

    print("Monthly analytics built successfully.")
    print(f"Source orders: {len(orders):,}")
    print(f"Analytics rows: {len(analytics):,}")
    print(f"Output: {OUTPUT_FILE}")
    print("\nPreview:")
    print(analytics.head(10).to_string(index=False))


if __name__ == "__main__":
    main()

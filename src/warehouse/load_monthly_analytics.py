
"""CommercePulse: load monthly analytics into PostgreSQL."""

from pathlib import Path
import os

import pandas as pd
import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "warehouse"
    / "monthly_order_analytics.parquet"
)


def load_monthly_analytics() -> int:
    """Load monthly analytics into PostgreSQL and return row count."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Analytics file not found: {INPUT_FILE}. "
            "Run the CommercePulse pipeline first."
        )

    analytics = pd.read_parquet(INPUT_FILE)

    required_columns = {
        "purchase_month",
        "order_status",
        "order_count",
    }

    if not required_columns.issubset(analytics.columns):
        raise ValueError(
            f"Analytics must contain these columns: {required_columns}"
        )

    database_url = os.getenv("COMMERCEPULSE_DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "COMMERCEPULSE_DATABASE_URL is not set."
        )

    rows = [
        (
            row.purchase_month,
            row.order_status,
            int(row.order_count),
        )
        for row in analytics.itertuples(index=False)
    ]

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO monthly_order_analytics (
                    purchase_month,
                    order_status,
                    order_count
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (purchase_month, order_status)
                DO UPDATE SET order_count = EXCLUDED.order_count
                """,
                rows,
            )

    return len(rows)


def main() -> None:
    """Run the warehouse load and display its result."""
    loaded_rows = load_monthly_analytics()
    print("PostgreSQL warehouse load completed successfully.")
    print(f"Analytics rows loaded: {loaded_rows:,}")


if __name__ == "__main__":
    main()


"""CommercePulse: initial order-data ingestion module."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_orders(file_path: str | Path) -> pd.DataFrame:
    """Load order data from a CSV file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Order data file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Expected a CSV file.")

    orders = pd.read_csv(path)

    if orders.empty:
        raise ValueError("The order data file is empty.")

    return orders

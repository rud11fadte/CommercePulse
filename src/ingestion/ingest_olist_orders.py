
"""CommercePulse: ingest and validate the Olist orders dataset."""

import logging
import time
from pathlib import Path

import pandas as pd

from src.quality.validate_orders import validate_orders


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "olist_orders.parquet"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "ingestion.log"


def configure_logging() -> None:
    """Write pipeline logs to both the terminal and a log file."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
        force=True,
    )


def main() -> None:
    """Load, validate, and store Olist order data."""
    configure_logging()
    logger = logging.getLogger(__name__)
    start_time = time.perf_counter()

    try:
        logger.info("Starting Olist order ingestion")

        if not RAW_FILE.exists():
            raise FileNotFoundError(f"Dataset not found: {RAW_FILE}")

        orders = pd.read_csv(RAW_FILE)
        logger.info(
            "Loaded %s rows and %s columns",
            len(orders),
            len(orders.columns),
        )

        errors = validate_orders(orders)

        if errors:
            for error in errors:
                logger.error("Data-quality check failed: %s", error)
            raise ValueError("Order data failed validation")

        logger.info("Data-quality validation passed")

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        orders.to_parquet(OUTPUT_FILE, index=False)

        elapsed = time.perf_counter() - start_time
        logger.info("Parquet output saved to %s", OUTPUT_FILE)
        logger.info("Rows written: %s", len(orders))
        logger.info("Run completed in %.2f seconds", elapsed)

    except Exception:
        logger.exception("Olist order ingestion failed")
        raise


if __name__ == "__main__":
    main()


"""CommercePulse: execute the complete analytics pipeline."""

import logging
import subprocess
import sys


PIPELINE_STEPS = [
    ("Order ingestion and validation", "src.ingestion.ingest_olist_orders"),
    ("Monthly analytics generation", "src.processing.build_monthly_analytics"),
    ("Data quality report generation", "src.quality.quality_report"),
    ("PostgreSQL warehouse loading", "src.warehouse.load_monthly_analytics"),
]


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("commercepulse")

    logger.info("CommercePulse pipeline started")

    for step_name, module_name in PIPELINE_STEPS:
        logger.info("Starting: %s", step_name)

        result = subprocess.run(
            [sys.executable, "-m", module_name],
            check=False,
        )

        if result.returncode != 0:
            logger.error("Pipeline failed at: %s", step_name)
            return result.returncode

        logger.info("Completed: %s", step_name)

    logger.info("All four pipeline steps completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

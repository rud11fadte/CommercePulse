
"""CommercePulse: run the complete batch analytics pipeline."""

import logging
import subprocess
import sys


PIPELINE_STEPS = [
    (
        "Order ingestion and data-quality validation",
        "src.ingestion.ingest_olist_orders",
    ),
    (
        "Monthly order analytics",
        "src.processing.build_monthly_analytics",
    ),
    (
        "Data quality report generation",
        "src.quality.quality_report",
    ),
]


def main() -> int:
    """Execute pipeline steps in order and stop on failure."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("commercepulse")

    logger.info("CommercePulse pipeline started")

    for step_name, module_name in PIPELINE_STEPS:
        logger.info("Starting step: %s", step_name)

        result = subprocess.run(
            [sys.executable, "-m", module_name],
            check=False,
        )

        if result.returncode != 0:
            logger.error(
                "Pipeline stopped because this step failed: %s",
                step_name,
            )
            return result.returncode

        logger.info("Completed step: %s", step_name)

    logger.info("CommercePulse pipeline completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

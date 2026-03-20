"""
anomaly_detector_web_service_metrics.py - Project script.

Author: Branton J. Dawson
Date: 2026-03-20

Static Data

- Data is taken from web service operational metrics.
- The data is static and each row represents one time interval.
- Key fields:
  - timestamp: interval marker
  - requests: request volume in the interval
  - errors: count of failed requests
  - total_latency_ms: aggregate latency in milliseconds

Purpose

- Read web-service metrics from CSV.
- Detect intervals with suspicious load, error rate, or latency.
- Save anomalies and reasons to artifacts for review.

Paths (relative to repo root)

    INPUT FILE: data/web-service-metrics.csv
    OUTPUT FILE: artifacts/anomalies_web_service_metrics.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.anomaly_detector_web_service_metrics
"""

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

LOG: logging.Logger = get_logger("P2", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "web-service-metrics.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "anomalies_web_service_metrics.csv"


def main() -> None:
    """Run the pipeline for web-service metric anomalies."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    df: pl.DataFrame = pl.read_csv(DATA_FILE)
    LOG.info(f"Loaded {df.height} metric rows")

    # Thresholds can be tuned as operating baselines evolve.
    MAX_REQUESTS: Final[int] = 200
    MAX_ERROR_RATE: Final[float] = 0.04
    MAX_TOTAL_LATENCY_MS: Final[int] = 8000

    LOG.info(f"MAX_REQUESTS: {MAX_REQUESTS}")
    LOG.info(f"MAX_ERROR_RATE: {MAX_ERROR_RATE}")
    LOG.info(f"MAX_TOTAL_LATENCY_MS: {MAX_TOTAL_LATENCY_MS}")

    analyzed_df = df.with_columns(
        (pl.col("errors") / pl.col("requests")).alias("error_rate")
    )

    anomalies_df: pl.DataFrame = analyzed_df.filter(
        (pl.col("requests") > MAX_REQUESTS)
        | (pl.col("error_rate") > MAX_ERROR_RATE)
        | (pl.col("total_latency_ms") > MAX_TOTAL_LATENCY_MS)
    )

    anomalies_df = anomalies_df.with_columns(
        pl.when(
            (pl.col("requests") > MAX_REQUESTS)
            & (pl.col("error_rate") > MAX_ERROR_RATE)
            & (pl.col("total_latency_ms") > MAX_TOTAL_LATENCY_MS)
        )
        .then(pl.lit("high traffic; high error rate; high latency"))
        .when(
            (pl.col("requests") > MAX_REQUESTS)
            & (pl.col("error_rate") > MAX_ERROR_RATE)
        )
        .then(pl.lit("high traffic; high error rate"))
        .when(
            (pl.col("requests") > MAX_REQUESTS)
            & (pl.col("total_latency_ms") > MAX_TOTAL_LATENCY_MS)
        )
        .then(pl.lit("high traffic; high latency"))
        .when(
            (pl.col("error_rate") > MAX_ERROR_RATE)
            & (pl.col("total_latency_ms") > MAX_TOTAL_LATENCY_MS)
        )
        .then(pl.lit("high error rate; high latency"))
        .when(pl.col("requests") > MAX_REQUESTS)
        .then(pl.lit("high traffic"))
        .when(pl.col("error_rate") > MAX_ERROR_RATE)
        .then(pl.lit("high error rate"))
        .otherwise(pl.lit("high latency"))
        .alias("reason")
    )

    anomalies_df = anomalies_df.with_columns(
        pl.col("error_rate").round(4).alias("error_rate"),
        (pl.col("error_rate") * 100).round(2).alias("error_rate_pct"),
    )

    LOG.info(f"Count of anomalies found: {anomalies_df.height}")

    anomalies_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote anomalies file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


if __name__ == "__main__":
    main()

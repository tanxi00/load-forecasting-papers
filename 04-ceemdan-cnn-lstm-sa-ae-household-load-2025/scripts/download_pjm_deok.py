#!/usr/bin/env python3
"""Download hourly DEOK load from PJM Data Miner 2."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


API_URL = "https://api.pjm.com/api/v1/hrl_load_metered"
FIELDS = [
    "datetime_beginning_utc",
    "datetime_beginning_ept",
    "nerc_region",
    "mkt_region",
    "zone",
    "load_area",
    "mw",
    "is_verified",
]


def year_ranges(start: str, end: str):
    first = pd.Timestamp(start)
    last = pd.Timestamp(end)
    for year in range(first.year, last.year + 1):
        chunk_start = max(first, pd.Timestamp(year=year, month=1, day=1))
        chunk_end = min(last, pd.Timestamp(year=year, month=12, day=31))
        yield chunk_start, chunk_end


def fetch_chunk(api_key: str, start: pd.Timestamp, end: pd.Timestamp) -> list[dict]:
    params = {
        "rowCount": 50000,
        "startRow": 1,
        "sort": "datetime_beginning_ept",
        "order": "asc",
        "fields": ",".join(FIELDS),
        "zone": "DEOK",
        "datetime_beginning_ept": (
            f"{start:%m/%d/%Y %H:%M} to {end:%m/%d/%Y %H:%M}"
        ),
    }
    request = Request(
        f"{API_URL}?{urlencode(params)}",
        headers={
            "Ocp-Apim-Subscription-Key": api_key,
            "Accept": "application/json",
            "User-Agent": "load-forecasting-papers/1.0",
        },
    )
    with urlopen(request, timeout=180) as response:
        payload = json.load(response)
    rows = payload.get("items", [])
    total = int(payload.get("totalRows", len(rows)))
    if total > len(rows):
        raise RuntimeError(
            f"PJM returned {len(rows)} of {total} rows; pagination is required"
        )
    return rows


def prepare(rows: list[dict], output_path: Path) -> None:
    raw = pd.DataFrame(rows)
    raw = raw[raw["zone"] == "DEOK"].copy()
    raw["datetime_utc"] = pd.to_datetime(
        raw["datetime_beginning_utc"],
        format="%m/%d/%Y %I:%M:%S %p",
    )
    raw["datetime_ept"] = pd.to_datetime(
        raw["datetime_beginning_ept"],
        format="%m/%d/%Y %I:%M:%S %p",
    )
    raw["mw"] = pd.to_numeric(raw["mw"], errors="coerce")
    raw = raw.sort_values("datetime_utc").drop_duplicates("datetime_utc")
    raw = raw.set_index("datetime_utc")

    hourly_index = pd.date_range(raw.index.min(), raw.index.max(), freq="h")
    raw = raw.reindex(hourly_index)
    raw.index.name = "datetime_utc"
    raw["demand_mw_raw"] = raw["mw"]
    raw["demand_mw"] = raw["mw"].interpolate(method="time")
    raw["is_imputed"] = raw["demand_mw_raw"].isna().astype(int)
    raw["zone"] = raw["zone"].fillna("DEOK")
    raw["load_area"] = raw["load_area"].fillna("DEOK")

    result = raw.reset_index()
    result["datetime_ept"] = result["datetime_ept"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    result["datetime_utc"] = result["datetime_utc"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    result = result[
        [
            "datetime_utc",
            "datetime_ept",
            "nerc_region",
            "mkt_region",
            "zone",
            "load_area",
            "demand_mw_raw",
            "demand_mw",
            "is_imputed",
            "is_verified",
        ]
    ]
    result.to_csv(output_path, index=False)
    print(f"Saved {len(result):,} hourly rows to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-key",
        default=os.getenv("PJM_API_KEY"),
        help="PJM Data Miner 2 subscription key; defaults to PJM_API_KEY",
    )
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2026-10-22")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/pjm_deok_hourly.csv"),
    )
    args = parser.parse_args()
    if not args.api_key:
        parser.error("Provide --api-key or set PJM_API_KEY")

    rows: list[dict] = []
    for start, end in year_ranges(args.start, args.end):
        chunk = fetch_chunk(
            args.api_key,
            start.replace(hour=0, minute=0),
            end.replace(hour=23, minute=59),
        )
        print(f"{start.date()} to {end.date()}: {len(chunk):,} rows")
        rows.extend(chunk)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    prepare(rows, args.output)


if __name__ == "__main__":
    main()

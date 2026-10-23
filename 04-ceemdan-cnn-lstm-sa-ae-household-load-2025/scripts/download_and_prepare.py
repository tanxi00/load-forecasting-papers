#!/usr/bin/env python3
"""Download recent replacement data and prepare compact forecasting series.

Plegma is the recent household-load replacement for the paper's Sceaux
dataset. Plegma source timestamps use a fixed UTC+03 clock. The PJM DEOK
series is downloaded by ``download_pjm_deok.py``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def prepare_plegma(
    source_root: Path,
    output_dir: Path,
    start: str,
    end: str,
    houses: list[str],
) -> None:
    """Aggregate Plegma 10-second P_agg readings to 15-minute load."""
    frames: list[pd.DataFrame] = []

    for house in houses:
        electric_dir = source_root / house / "Electric_data"
        files = sorted(electric_dir.glob("20??-??.csv"))
        if not files:
            print(f"Skipping {house}: no monthly files")
            continue

        monthly: list[pd.DataFrame] = []
        for path in files:
            frame = pd.read_csv(path, usecols=["timestamp", "P_agg"])
            monthly.append(frame)

        raw = pd.concat(monthly, ignore_index=True)
        raw["timestamp"] = pd.to_datetime(raw["timestamp"], errors="coerce")
        raw["P_agg"] = pd.to_numeric(raw["P_agg"], errors="coerce")
        raw = raw.dropna().sort_values("timestamp")
        raw = raw[
            (raw["timestamp"] >= pd.Timestamp(start))
            & (raw["timestamp"] <= pd.Timestamp(end))
        ]
        if raw.empty:
            print(f"Skipping {house}: no readings in requested window")
            continue

        series = raw.set_index("timestamp")["P_agg"]
        load_kw = series.resample("15min").mean() / 1000.0
        sample_count = series.resample("15min").count()

        full_index = pd.date_range(
            load_kw.index.min().floor("15min"),
            load_kw.index.max().floor("15min"),
            freq="15min",
        )
        load_kw = load_kw.reindex(full_index)
        sample_count = sample_count.reindex(full_index, fill_value=0)

        raw_load_kw = load_kw.copy()
        load_kw = load_kw.interpolate(method="time", limit_area="inside")

        prepared = pd.DataFrame(
            {
                "house_id": house,
                "timestamp": full_index.strftime("%Y-%m-%d %H:%M:%S"),
                "raw_load_kw": raw_load_kw.to_numpy(),
                "load_kw": load_kw.to_numpy(),
                "energy_kwh": load_kw.to_numpy() * 0.25,
                "source_10s_samples": sample_count.to_numpy(),
                "source_coverage": (sample_count.to_numpy() / 90.0).round(4),
                "is_imputed": raw_load_kw.isna().astype(int).to_numpy(),
            }
        )
        frames.append(prepared)
        print(
            f"{house}: {len(prepared):,} intervals, "
            f"{prepared['is_imputed'].sum():,} imputed"
        )

    if not frames:
        raise RuntimeError("No Plegma data were prepared")

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(output_dir / "plegma_all_households_15min.csv", index=False)

    house01 = combined[combined["house_id"] == "House_01"]
    if not house01.empty:
        house01.to_csv(output_dir / "plegma_house01_15min.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plegma-root",
        type=Path,
        help="Path containing House_01 ... House_13 directories",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    parser.add_argument("--plegma-start", default="2022-07-01 00:00:00")
    parser.add_argument("--plegma-end", default="2023-09-30 23:59:50")
    parser.add_argument(
        "--houses",
        nargs="*",
        default=[f"House_{index:02d}" for index in range(1, 14)],
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.plegma_root:
        prepare_plegma(
            args.plegma_root,
            args.output_dir,
            args.plegma_start,
            args.plegma_end,
            args.houses,
        )
    if not args.plegma_root:
        parser.error("Provide --plegma-root")


if __name__ == "__main__":
    main()

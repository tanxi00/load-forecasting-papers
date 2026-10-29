from pathlib import Path

import h5py
import pandas as pd


RAW_DIR = Path(r"D:\GPT\2026-10-07\zh\work\raw\WPuQ")
OUTPUT_DIR = Path(r"D:\GPT(work)\date")


def read_household_loads(year):
    source = RAW_DIR / f"{year}_data_60min.hdf5"
    series = {}

    with h5py.File(source, "r") as handle:
        if "NO_PV" not in handle:
            raise ValueError(f"{source} does not contain NO_PV households")

        for household in sorted(handle["NO_PV"].keys(), key=lambda x: int(x[3:])):
            table = handle[f"NO_PV/{household}/HOUSEHOLD/table"][:]
            if "P_TOT" not in table.dtype.names:
                raise ValueError(f"{household} has no P_TOT field in {source}")

            index = pd.to_datetime(table["index"], unit="s", utc=True)
            values = pd.Series(table["P_TOT"], index=index, name=household)
            if values.index.has_duplicates:
                raise ValueError(f"{household} has duplicate timestamps in {source}")
            series[household] = values

    frame = pd.DataFrame(series).sort_index()
    expected = pd.date_range(frame.index.min(), frame.index.max(), freq="h")
    if not frame.index.equals(expected):
        raise ValueError(f"{year} hourly timestamps are not continuous")
    return frame


def main():
    data_2019 = read_household_loads(2019)
    data_2020 = read_household_loads(2020)
    common_columns = data_2019.columns.intersection(data_2020.columns, sort=False)
    data_2019 = data_2019[common_columns]
    data_2020 = data_2020[common_columns]

    households = pd.concat([data_2019, data_2020]).sort_index()
    if households.index.has_duplicates:
        raise ValueError("Combined data contains duplicate timestamps")

    inventory = pd.DataFrame({
        "household": households.columns,
        "missing_hours": households.isna().sum().to_numpy(),
        "minimum_w": households.min().to_numpy(),
        "maximum_w": households.max().to_numpy(),
    })
    inventory["selected"] = inventory["missing_hours"].eq(0)
    selected = inventory.loc[inventory["selected"], "household"].tolist()
    if not selected:
        raise ValueError("No complete households found")

    total_w = households[selected].sum(axis=1, min_count=len(selected))
    result = pd.DataFrame({
        "date": total_w.index.tz_convert("UTC").tz_localize(None),
        "load_kw": total_w.to_numpy() / 1000,
    })
    if result["load_kw"].isna().any():
        raise ValueError("Selected households still contain missing values")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(
        OUTPUT_DIR / "wpuq_household_hourly.csv",
        index=False,
        date_format="%Y-%m-%d %H:%M:%S",
    )
    inventory.to_csv(OUTPUT_DIR / "wpuq_household_inventory.csv", index=False)

    print(f"raw_households={len(inventory)}")
    print(f"complete_households={len(selected)}")
    print(f"selected={','.join(selected)}")
    print(f"rows={len(result)}")
    print(f"range={result['date'].min()} to {result['date'].max()}")
    print(f"load_kw_range={result['load_kw'].min()} to {result['load_kw'].max()}")


if __name__ == "__main__":
    main()
